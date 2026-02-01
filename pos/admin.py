from django.contrib import admin
from .models import *

# Custom admin classes
class StudentInvoiceAdmin(admin.ModelAdmin):
    list_display = ('student', 'present_invoice_no', 'pending_invoice_no', 'created_at', 'updated_at')
    search_fields = ('student__name', 'student__email', 'student__phone')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        # Prefetch related student data to avoid N+1 queries
        return super().get_queryset(request).select_related('student')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'batch', 'payment_status', 'discounted_price', 'advance_payment', 'second_installment', 'balance', 'second_installment_due_date')
    list_filter = ('payment_status', 'batch', 'created_at')
    search_fields = ('name', 'phone_number', 'cnic')
    readonly_fields = ('created_at', 'updated_at')

# Register your models here.
admin.site.register(Course)
admin.site.register(Student, StudentAdmin)
admin.site.register(CSRProfile)
admin.site.register(InvoiceSettings)
admin.site.register(StudentInvoice, StudentInvoiceAdmin)
