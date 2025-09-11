from django.core.management.base import BaseCommand
from example.models import Student

class Command(BaseCommand):
    help = 'Update balance field for all existing student records'

    def handle(self, *args, **options):
        # Get all student records
        students = Student.objects.all()
        updated_count = 0
        
        for student in students:
            if student.payment_status == 'pending':
                # For pending payments, set balance equal to second_installment
                student.balance = student.second_installment
                student.save(update_fields=['balance'])
                updated_count += 1
            elif student.payment_status == 'paid':
                # For paid payments, set balance to 0
                student.balance = 0
                student.save(update_fields=['balance'])
                updated_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated balance for {updated_count} students'))
