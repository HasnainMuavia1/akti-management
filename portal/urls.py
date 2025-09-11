from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.portal_dashboard, name='portal_dashboard'),
    path('login/', views.portal_login, name='portal_login'),
    path('logout/', views.portal_logout, name='portal_logout'),

    # Admin
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/trainers/', views.trainer_management, name='trainer_management'),
    path('admin/trainers/add/', views.trainer_add, name='trainer_add'),
    path('admin/trainers/<int:trainer_id>/edit/', views.trainer_edit, name='trainer_edit'),
    path('admin/trainers/<int:trainer_id>/delete/', views.trainer_delete, name='trainer_delete'),

    path('admin/course-assignment/', views.course_assignment, name='course_assignment'),
    path('admin/course-assignment/form/', views.course_assignment_form, name='course_assignment_form'),
    path('admin/course-assignment/<int:assignment_id>/delete/', views.delete_assignment, name='delete_assignment'),

    path('admin/individual-attendance/', views.individual_attendance, name='individual_attendance'),
    path('admin/student/<int:student_id>/', views.student_details, name='student_details'),
    path('admin/course-reports/', views.course_attendance_report, name='course_attendance_report'),
    path('admin/batch-attendance-report/', views.batch_attendance_report, name='batch_attendance_report'),

    # Trainer
    path('trainer/dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
    path('trainer/course/<int:trainer_course_id>/', views.trainer_course_detail, name='trainer_course_detail'),
    path('trainer/course/<int:trainer_course_id>/attendance/start/', views.trainer_start_attendance, name='trainer_start_attendance'),
    path('trainer/course/<int:trainer_course_id>/attendance/create-for-date/', views.trainer_create_attendance_for_date, name='trainer_create_attendance_for_date'),
    path('trainer/attendance/<int:lecture_id>/', views.mark_attendance, name='mark_attendance'),
    path('trainer/reports/', views.trainer_reports, name='trainer_reports'),

    # Reports download
    path('download/<str:report_type>/', views.download_attendance_report, name='download_report_no_id'),
    path('download/<str:report_type>/<int:object_id>/', views.download_attendance_report, name='download_report'),

    # AJAX
    path('ajax/mark-attendance/', views.ajax_mark_attendance, name='ajax_mark_attendance'),
]
