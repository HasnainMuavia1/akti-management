from django.core.management.base import BaseCommand
from example.models import Student, StudentInvoice
from django.db import transaction
from django.utils import timezone


class Command(BaseCommand):
    help = 'Migrates existing students to the StudentInvoice model'

    def handle(self, *args, **options):
        # Get all students
        students = Student.objects.all()
        created_count = 0
        skipped_count = 0
        
        self.stdout.write(self.style.SUCCESS(f'Found {students.count()} students to process'))
        
        with transaction.atomic():
            for student in students:
                # Check if student already has an invoice record
                invoice_exists = StudentInvoice.objects.filter(student=student).exists()
                
                if invoice_exists:
                    skipped_count += 1
                    continue
                
                # Create new StudentInvoice record
                invoice = StudentInvoice(
                    student=student,
                    created_at=timezone.now()
                )
                
                # If student has an existing invoice number, try to parse it
                if student.invoice_number:
                    try:
                        # Check if it's a pending invoice (starts with P)
                        if student.invoice_number.startswith('P'):
                            # Remove the P prefix and convert to integer
                            invoice.pending_invoice_no = int(student.invoice_number[1:])
                        else:
                            # Regular invoice, convert to integer
                            invoice.present_invoice_no = int(student.invoice_number)
                    except (ValueError, TypeError):
                        # If conversion fails, just use 0 (default)
                        self.stdout.write(self.style.WARNING(
                            f'Could not parse invoice number "{student.invoice_number}" for student {student.name}'
                        ))
                
                # Save the invoice record
                invoice.save()
                created_count += 1
                
                # Progress indicator for large datasets
                if created_count % 100 == 0:
                    self.stdout.write(f'Processed {created_count} students...')
        
        self.stdout.write(self.style.SUCCESS(
            f'Migration complete! Created {created_count} invoice records, skipped {skipped_count} existing records'
        ))
