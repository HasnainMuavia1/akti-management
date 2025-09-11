from django.core.management.base import BaseCommand
from example.models import Student
from django.utils import timezone
from django.db import connection


class Command(BaseCommand):
    help = 'Transfers due_date values to second_installment_due_date and sets due_date to dash'

    def handle(self, *args, **options):
        # First check if second_installment_due_date field exists in the database
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='example_student' 
                AND column_name='second_installment_due_date'
            """)
            if not cursor.fetchone():
                self.stdout.write(self.style.ERROR(
                    'The second_installment_due_date field does not exist in the database. '
                    'Please run migrations first with: python manage.py migrate'
                ))
                return

        # Count students with due_date values
        students_with_due_date = Student.objects.filter(due_date__isnull=False).count()
        self.stdout.write(f"Found {students_with_due_date} students with due_date values to transfer")

        # Process each student individually to handle the date transfer
        updated_count = 0
        for student in Student.objects.filter(due_date__isnull=False):
            if not student.second_installment_due_date:
                student.second_installment_due_date = student.due_date
                updated_count += 1
            # We can't set a dash directly in a DateField, so we'll handle this in the template display
            student.due_date = None
            student.save()
        
        self.stdout.write(f"Transferred {updated_count} due_date values to second_installment_due_date")
        self.stdout.write(f"Set due_date to null for {students_with_due_date} students")
        self.stdout.write(self.style.SUCCESS('Successfully transferred due dates'))
