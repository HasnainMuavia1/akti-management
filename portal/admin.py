from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Trainer, TrainerCourse, Lecture, Attendance, AttendanceReport


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'email', 'assigned_courses_count', 'total_students', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'
    
    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'is_active')
        }),
        ('User Account', {
            'fields': ('user',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TrainerCourse)
class TrainerCourseAdmin(admin.ModelAdmin):
    list_display = ['trainer', 'course', 'total_lectures', 'completed_lectures', 'progress_percentage', 'assigned_at', 'is_active']
    list_filter = ['is_active', 'assigned_at', 'course__duration']
    search_fields = ['trainer__name', 'course__name']
    readonly_fields = ['assigned_at', 'total_lectures', 'completed_lectures', 'progress_percentage']
    
    fieldsets = (
        ('Assignment', {
            'fields': ('trainer', 'course', 'batch', 'schedule', 'is_active')
        }),
        ('Progress Information', {
            'fields': ('total_lectures', 'completed_lectures', 'progress_percentage'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('assigned_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ['lecture_number', 'trainer_course', 'date', 'start_time', 'end_time', 'duration_minutes', 'attendance_count']
    list_filter = ['date', 'trainer_course__course__duration']
    search_fields = ['trainer_course__trainer__name', 'trainer_course__course__name']
    readonly_fields = ['created_at', 'updated_at', 'duration_minutes', 'attendance_count']
    date_hierarchy = 'date'
    
    def attendance_count(self, obj):
        return obj.attendances.count()
    attendance_count.short_description = 'Attendance Count'
    
    fieldsets = (
        ('Lecture Information', {
            'fields': ('trainer_course', 'lecture_number', 'date', 'start_time', 'end_time')
        }),
        ('Statistics', {
            'fields': ('duration_minutes', 'attendance_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'lecture', 'status', 'marked_by', 'marked_at']
    list_filter = ['status', 'marked_at', 'lecture__trainer_course__course__duration']
    search_fields = ['student__name', 'lecture__trainer_course__trainer__name', 'lecture__trainer_course__course__name']
    readonly_fields = ['marked_at']
    date_hierarchy = 'marked_at'
    
    fieldsets = (
        ('Attendance Information', {
            'fields': ('lecture', 'student', 'status')
        }),
        ('Record Information', {
            'fields': ('marked_by', 'marked_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'generated_by', 'generated_at', 'download_link']
    list_filter = ['report_type', 'generated_at']
    search_fields = ['title', 'description', 'generated_by__username']
    readonly_fields = ['generated_at', 'download_link']
    date_hierarchy = 'generated_at'
    
    def download_link(self, obj):
        if obj.file_path:
            return format_html('<a href="{}" target="_blank">Download</a>', obj.file_path)
        return "No file"
    download_link.short_description = 'Download'
    
    fieldsets = (
        ('Report Information', {
            'fields': ('report_type', 'title', 'description')
        }),
        ('File Information', {
            'fields': ('file_path', 'download_link'),
            'classes': ('collapse',)
        }),
        ('Generation Information', {
            'fields': ('generated_by', 'generated_at'),
            'classes': ('collapse',)
        }),
    )
