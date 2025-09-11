from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from example.models import Course, Student, Batch


class Trainer(models.Model):
    """Model for storing trainer information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def assigned_courses_count(self):
        return self.trainer_courses.count()
    
    @property
    def total_students(self):
        total = 0
        for trainer_course in self.trainer_courses.all():
            total += trainer_course.course.students.count()
        return total


class TrainerCourse(models.Model):
    """Model for assigning courses to trainers"""
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='trainer_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='trainer_assignments')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='trainer_courses', null=True, blank=True)
    schedule = models.CharField(max_length=15, choices=Student.SCHEDULE_CHOICES, null=True, blank=True, help_text="Schedule for this assignment (weekdays/weekend)")
    assigned_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['trainer', 'course', 'batch']
        verbose_name = "Trainer Course Assignment"
        verbose_name_plural = "Trainer Course Assignments"
    
    def __str__(self):
        if self.batch:
            schedule_info = f" - {self.schedule}" if self.schedule else ""
            return f"{self.trainer.name} - {self.course.name} - Batch {self.batch.batch_number}{schedule_info}"
        schedule_info = f" - {self.schedule}" if self.schedule else ""
        return f"{self.trainer.name} - {self.course.name}{schedule_info}"
    
    @property
    def total_lectures(self):
        """Calculate total lectures based on course duration"""
        if '1_month' in self.course.duration:
            return 12
        else:  # weekend or weekdays
            return 24
    
    @property
    def completed_lectures(self):
        """Get count of lectures that have any attendance recorded"""
        return self.lectures.filter(attendances__isnull=False).distinct().count()
    
    @property
    def progress_percentage(self):
        """Calculate progress percentage"""
        if self.total_lectures == 0:
            return 0
        return round((self.completed_lectures / self.total_lectures) * 100, 1)


class Lecture(models.Model):
    """Model for individual lectures"""
    trainer_course = models.ForeignKey(TrainerCourse, on_delete=models.CASCADE, related_name='lectures')
    lecture_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['trainer_course', 'lecture_number']
        ordering = ['lecture_number']
    
    def __str__(self):
        return f"Lecture {self.lecture_number} - {self.trainer_course.course.name}"
    
    @property
    def duration_minutes(self):
        """Calculate lecture duration in minutes"""
        start = self.start_time
        end = self.end_time
        
        # Convert to minutes since midnight
        start_minutes = start.hour * 60 + start.minute
        end_minutes = end.hour * 60 + end.minute
        
        # Handle case where lecture goes past midnight
        if end_minutes < start_minutes:
            end_minutes += 24 * 60
            
        return end_minutes - start_minutes


class Attendance(models.Model):
    """Model for student attendance records"""
    ATTENDANCE_STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]
    
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS_CHOICES, default='present')
    marked_by = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='marked_attendances')
    marked_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['lecture', 'student']
        verbose_name = "Student Attendance"
        verbose_name_plural = "Student Attendances"
    
    def __str__(self):
        return f"{self.student.name} - {self.lecture} - {self.status}"
    
    @property
    def is_present(self):
        """Check if student was present."""
        return self.status == 'present'


class AttendanceReport(models.Model):
    """Model for storing attendance reports"""
    REPORT_TYPE_CHOICES = [
        ('course', 'Course Report'),
        ('batch', 'Batch Report'),
        ('student', 'Student Report'),
        ('trainer', 'Trainer Report'),
    ]
    
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file_path = models.CharField(max_length=500, blank=True)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_reports')
    generated_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.title} - {self.report_type}"
    
    @property
    def file_name(self):
        """Extract filename from file path"""
        if self.file_path:
            return self.file_path.split('/')[-1]
        return "No file"
