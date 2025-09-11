from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Trainer, TrainerCourse, Lecture, Attendance
from example.models import Course, Batch


class TrainerCreationForm(UserCreationForm):
    """Form for creating a new trainer with user account"""
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent',
        'placeholder': 'Enter trainer name'
    }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style all fields
        for field_name, field in self.fields.items():
            if field_name not in ['name']:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent'
                })
                if field_name == 'username':
                    field.widget.attrs['placeholder'] = 'Enter username'
                elif field_name == 'email':
                    field.widget.attrs['placeholder'] = 'Enter email address'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create trainer profile
            Trainer.objects.create(
                user=user,
                name=self.cleaned_data['name']
            )
        return user


class TrainerCourseAssignmentForm(forms.ModelForm):
    """Form for assigning courses to trainers"""
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.filter(is_active=True) if hasattr(Course, 'is_active') else Course.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'space-y-2'
        }),
        help_text="Select one or more courses to assign to this trainer"
    )
    batch = forms.ModelChoiceField(
        queryset=Batch.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent'
        })
    )
    schedule = forms.ChoiceField(
        choices=(('weekdays', 'Weekdays'), ('weekend', 'Weekend')),
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent'
        })
    )
    
    class Meta:
        model = TrainerCourse
        fields = ['trainer', 'batch', 'courses']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trainer'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent'
        })
    
    def save(self, commit=True):
        # This form will create multiple TrainerCourse objects
        instances = []
        trainer = self.cleaned_data['trainer']
        batch = self.cleaned_data['batch']
        courses = self.cleaned_data['courses']
        schedule = self.cleaned_data.get('schedule')
        
        for course in courses:
            assignment, created = TrainerCourse.objects.get_or_create(
                trainer=trainer,
                course=course,
                batch=batch,
                defaults={'is_active': True, 'schedule': schedule}
            )
            if not created:
                assignment.is_active = True
                if schedule:
                    assignment.schedule = schedule
            assignment.save()
            instances.append(assignment)
        
        return instances


class LectureForm(forms.ModelForm):
    """Form for creating/editing lectures"""
    class Meta:
        model = Lecture
        fields = ['lecture_number', 'date', 'start_time', 'end_time']
        widgets = {
            'lecture_number': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent'
            }),
            'date': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent',
                'type': 'date'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent',
                'type': 'time'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise ValidationError("End time must be after start time")
        
        return cleaned_data


class AttendanceForm(forms.ModelForm):
    """Form for marking attendance"""
    class Meta:
        model = Attendance
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent'
            })
        }


class BulkAttendanceForm(forms.Form):
    """Form for bulk attendance marking"""
    lecture = forms.ModelChoiceField(
        queryset=Lecture.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent'
        })
    )
    
    def __init__(self, trainer=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if trainer:
            # Filter lectures to only show those assigned to the trainer
            self.fields['lecture'].queryset = Lecture.objects.filter(
                trainer_course__trainer=trainer
            )


class CourseFilterForm(forms.Form):
    """Form for filtering courses in reports"""
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=False,
        empty_label="All Courses",
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent',
            'type': 'date'
        })
    )


class BatchFilterForm(forms.Form):
    """Form for filtering batches in reports"""
    batch = forms.ModelChoiceField(
        queryset=Course.objects.none(),  # Will be set in __init__
        required=False,
        empty_label="All Batches",
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get all batches from the example app
        from example.models import Batch
        self.fields['batch'].queryset = Batch.objects.all()


class TrainerEditForm(forms.ModelForm):
    """Form for editing an existing trainer and linked user"""
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent',
        'placeholder': 'Enter trainer name'
    }))
    new_password1 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent',
        'placeholder': 'New password (optional)'
    }))
    new_password2 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent',
        'placeholder': 'Confirm new password'
    }))

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        trainer = kwargs.pop('trainer', None)
        super().__init__(*args, **kwargs)
        # Style username/email
        for field_name, field in self.fields.items():
            if field_name not in ['name', 'new_password1', 'new_password2']:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-border rounded-md bg-input text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent'
                })
        if trainer is not None:
            self.fields['name'].initial = trainer.name

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('new_password1')
        p2 = cleaned_data.get('new_password2')
        if p1 or p2:
            if p1 != p2:
                raise ValidationError('Passwords do not match')
        return cleaned_data

    def save(self, trainer: Trainer, commit=True):
        user = super().save(commit=False)
        # user is the same instance passed via instance=... so updates apply
        if commit:
            user.save()
            # Update trainer name
            trainer.name = self.cleaned_data['name']
            trainer.save()
            # Update password if provided
            new_password = self.cleaned_data.get('new_password1')
            if new_password:
                user.set_password(new_password)
                user.save()
        return user
