from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('toggle-dark-mode/', views.toggle_dark_mode, name='toggle_dark_mode'),
    
    # Admin Dashboard URLs
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/commission/', views.commission_report, name='commission_report'),
    path('dashboard/csr/', views.csr_management, name='csr_management'),
    path('dashboard/courses/', views.course_management, name='course_management'),
    path('dashboard/batches/', views.admin_batch_management, name='admin_batch_management'),
    path('dashboard/batches/<int:batch_id>/update-status/', views.update_batch_status, name='update_batch_status'),
    
    # Report Generation URLs
    path('reports/students/', views.report_students, name='report_students'),
    path('reports/students/ajax/', views.report_students_ajax, name='report_students_ajax'),
    path('reports/revenue/', views.report_revenue, name='report_revenue'),
    path('reports/revenue/ajax/', views.report_revenue_ajax, name='report_revenue_ajax'),
    
    # API Endpoints
    path('api/batch-stats/', views.get_batch_stats, name='get_batch_stats'),
    
    # CSR Report URLs
    path('csr/reports/students/', views.report_students, name='report_students_csr'),
    path('csr/reports/revenue/', views.report_revenue, name='report_revenue_csr'),
    path('csr/courses/', views.csr_course_management, name='course_management_csr'),
    
    # CSR Dashboard URLs
    path('csr/dashboard/', views.csr_dashboard, name='csr_dashboard'),
    path('csr/batches/', views.csr_batch_management, name='csr_batch_management'),
    path('csr/batches/old/', views.batch_management, name='batch_management'),
    path('csr/students/', views.student_management, name='student_management'),
    path('csr/students/<int:student_id>/invoice/', views.generate_invoice, name='generate_invoice'),
    path('csr/students/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('csr/students/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    path('csr/students/<int:student_id>/update-payment-status/', views.update_payment_status, name='update_payment_status'),
    path('csr/students/<int:student_id>/pending-invoice/', views.generate_pending_invoice, name='generate_pending_invoice'),
    path('csr/settings/', views.invoice_settings, name='invoice_settings'),
    
    # Password Change URL (for both admin and CSR)
    path('change-password/', views.change_password, name='change_password'),
]