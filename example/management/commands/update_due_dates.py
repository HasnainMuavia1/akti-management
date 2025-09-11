from django.core.management.base import BaseCommand
from example.models import Student
from django.db.models import F


class Command(BaseCommand):
    help = 'Updates due_date to match created_at for students who paid in full at once'

    def handle(self, *args, **options):
        self.stdout.write("Starting due date update for full payment students...")

        # Find students who paid in full at once (advance_payment equals discounted_price)
        full_payment_students = Student.objects.filter(
            advance_payment=F('discounted_price')
        )

        count = full_payment_students.count()
        self.stdout.write(f"Found {count} students who paid in full at once")

        # Update due_date to match created_at for these students
        updated_count = 0
        for student in full_payment_students:
            if student.created_at:
                student.due_date = student.created_at
                student.save(update_fields=['due_date'])
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(f"Updated due_date for {updated_count} students"))
        self.stdout.write(self.style.SUCCESS("Successfully completed due date updates"))
