from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import User


class Course(models.Model):
    # Store comma-separated schedule/duration values (e.g., "weekend,1_month")
    name = models.CharField(max_length=100)
    trainer_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price in PKR')
    duration = models.CharField(max_length=100, help_text='Comma-separated schedule/duration tags')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class CSRProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='csr_profile')
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    lead_role = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.full_name
    
    def get_full_name(self):
        return self.full_name
    
    @property
    def invoice_count(self):
        return self.invoices.count() if hasattr(self, 'invoices') else 0



    @property
    def student_count(self):
        return self.students.count() if hasattr(self, 'students') else 0


class Batch(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    batch_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', help_text="Batch status - inactive batches are considered completed")
    created_by = models.ForeignKey(CSRProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='batches')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Batch {self.batch_number}"
    
    @property
    def student_count(self):
        return self.students.count()


class Student(models.Model):
    """Student model for storing student information"""
    SCHEDULE_CHOICES = [
        ('weekend', 'Weekend'),
        ('weekdays', 'Weekdays'),
        ('1_month', '1 Month'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('online', 'Online Payment'),
    ]
    
    name = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15)
    cnic = models.CharField(max_length=15, blank=True, help_text="CNIC or B-Form number")
    courses = models.ManyToManyField(Course, related_name='students')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='students')
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)], help_text="Discount percentage")
    total_fees = models.IntegerField(validators=[MinValueValidator(0)])
    discounted_price = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    advance_payment = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_amount = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Total amount including advance payment and second installment")
    schedule = models.CharField(max_length=15, choices=SCHEDULE_CHOICES, default='weekend')
    second_installment = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    balance = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Balance amount to be paid")
    second_installment_due_date = models.DateField(null=True, blank=True, help_text="Due date for second installment payment")
    due_date = models.DateField(null=True, blank=True, help_text="Date when pending invoice was generated")
    invoice_number = models.CharField(max_length=50, blank=True, null=True, help_text="Unique invoice number for this student")
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='cash', help_text="Payment method used by the student")
    # Persist creator CSR name so it remains if CSR profile is deleted
    created_by_name = models.CharField(max_length=100, blank=True, help_text="Name of CSR who enrolled the student (immutable)")
    created_by = models.ForeignKey(CSRProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        """Persist creator CSR name and handle payment status changes."""
        # Check if this is an existing record being updated
        if self.pk:
            # Get the original object from the database
            try:
                original = Student.objects.get(pk=self.pk)
                
                # If payment status is changing from pending to paid
                if original.payment_status == 'pending' and self.payment_status == 'paid':
                    # Set balance to 0 when payment status changes to paid
                    # But keep second_installment value for record-keeping
                    self.balance = 0
                    # Update total_amount to include both advance payment and second installment
                    self.total_amount = self.advance_payment + self.second_installment
                
                # If payment status is changing from paid to pending
                elif original.payment_status == 'paid' and self.payment_status == 'pending':
                    # Restore balance to match second_installment when going back to pending
                    self.balance = self.second_installment
                    # Reset total_amount to just advance payment
                    self.total_amount = self.advance_payment
            except Student.DoesNotExist:
                pass
        else:
            # For new records, initialize balance to match second_installment
            self.balance = self.second_installment
            
            # For new records, set total_amount based on payment status
            if self.payment_status == 'pending':
                self.total_amount = self.advance_payment
            else:  # 'paid'
                self.total_amount = self.advance_payment + self.second_installment
        
        # Persist creator CSR name
        if not self.created_by_name and self.created_by:
            self.created_by_name = self.created_by.get_full_name()
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_creator_name(self):
        """Return the name of the CSR who enrolled the student, falling back to stored value."""
        # If CSR still exists, prefer its current full name
        if self.created_by:
            # If local cache missing, backfill it
            if not self.created_by_name:
                self.created_by_name = self.created_by.get_full_name()
                super().save(update_fields=["created_by_name"])
            return self.created_by.get_full_name()
        # Fallback to stored name
        return self.created_by_name or "Unknown"

    @property
    def remaining_balance(self):
        # Return the balance field which will be 0 when payment_status is 'paid'
        # or will match second_installment when payment_status is 'pending'
        return self.balance


class InvoiceSettings(models.Model):
    """Model to store CSR-specific invoice settings"""
    csr = models.OneToOneField(CSRProfile, on_delete=models.CASCADE, related_name='invoice_settings')
    
    # Serial number settings
    current_serial_number = models.PositiveIntegerField(default=1000, validators=[MinValueValidator(1)])
    
    # Bank details
    school_name = models.CharField(max_length=255, default='Arfa Karim Technology Incubator Pvt Ltd ')
    bank_name = models.CharField(max_length=100, default='JS Bank')
    account_number = models.CharField(max_length=50, default='0002587773')
    iban_number = models.CharField(max_length=50, default='PK56JSBL9561000002587773')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.csr.full_name}'s Invoice Settings"
    
    def get_current_serial_number(self):
        """Get the current serial number without incrementing"""
        return f"{self.current_serial_number}"
        
    def increment_serial_number(self):
        """Increment the serial number counter and save"""
        self.current_serial_number += 1
        self.save()
        
    def get_next_serial_number(self):
        """DEPRECATED: Use get_current_serial_number() instead.
        This method is kept for backward compatibility."""
        return self.get_current_serial_number()


class StudentInvoice(models.Model):
    """
    Model to track invoice numbers for both regular and pending invoices.
    Each student can have one regular invoice number and one pending invoice number.
    Invoice numbers are only incremented when they are 0 (not yet generated).
    """
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='invoice_numbers')
    present_invoice_no = models.IntegerField(default=0, help_text="Regular invoice number, 0 means not yet generated")
    pending_invoice_no = models.IntegerField(default=0, help_text="Pending payment invoice number, 0 means not yet generated")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Invoice for {self.student.name}"
    
    class Meta:
        verbose_name = "Student Invoice"
        verbose_name_plural = "Student Invoices"
