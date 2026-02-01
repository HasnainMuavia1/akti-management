from django import forms
from .models import Student, Course, Batch, InvoiceSettings


class StudentForm(forms.ModelForm):
    """Form for creating and editing students"""
    
    # Make due_date optional with a widget
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    
    # Use a read-only field for total_fees as it will be calculated automatically
    total_fees = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        required=False
    )
    
    # Add a visible field for discounted price
    discounted_price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        required=False
    )
    
    # Use a visible field for second_installment as it will be calculated automatically
    second_installment = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
        required=False
    )
    
    class Meta:
        model = Student
        fields = [
            'name', 'guardian_name', 'phone_number', 'cnic',
            'batch', 'courses', 'discount', 'total_fees',
            'discounted_price', 'advance_payment', 'second_installment', 'balance',
            'total_amount', 'payment_status', 'due_date', 'second_installment_due_date',
            'schedule'
        ]
        widgets = {
            'courses': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'batch': forms.Select(attrs={'class': 'form-select'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Discount %', 'step': '0.01', 'min': '0', 'max': '100'}),
            'advance_payment': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['due_date'].required = False
        self.fields['discount'].label = 'Discount (%)'
        self.fields['total_fees'].label = 'Total Fees (PKR)'
        self.fields['discounted_price'].label = 'Discounted Price (PKR)'
        self.fields['second_installment'].label = 'Pending Payment (PKR)'
        
    def clean(self):
        cleaned_data = super().clean()
        courses = cleaned_data.get('courses')
        discount_percent = cleaned_data.get('discount', 0)
        advance_payment = cleaned_data.get('advance_payment', 0)
        payment_status = cleaned_data.get('payment_status', 'pending')
        
        # Calculate total fees from selected courses
        total_fees = 0
        if courses:
            for course in courses:
                total_fees += course.price
        
        # Apply discount as percentage
        discount_amount = (total_fees * discount_percent / 100) if discount_percent else 0
        discounted_price = total_fees - discount_amount
        
        # Calculate second installment (pending payment)
        second_installment = max(0, discounted_price - advance_payment)
        
        # Set balance equal to second_installment
        balance = second_installment
        
        # Set total_amount based on payment status
        total_amount = advance_payment
        if payment_status == 'paid':
            total_amount = discounted_price
        
        # Set the calculated values
        cleaned_data['total_fees'] = total_fees
        cleaned_data['discounted_price'] = discounted_price
        cleaned_data['second_installment'] = second_installment
        cleaned_data['balance'] = balance
        cleaned_data['total_amount'] = total_amount
        
        return cleaned_data


class InvoiceSettingsForm(forms.ModelForm):
    """Form for managing invoice settings"""
    class Meta:
        model = InvoiceSettings
        fields = [
            'current_serial_number',
            'school_name', 'bank_name',
            'account_number', 'iban_number',
        ]
        widgets = {
            'current_serial_number': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'school_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'iban_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
