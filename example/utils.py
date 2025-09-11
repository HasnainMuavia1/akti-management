from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from django.conf import settings
from .models import InvoiceSettings, StudentInvoice
import os
import pytz

# Removed ReportLab table styles and flowables


def get_invoice_context(student, is_pending=False):
    """
    Prepare context data for HTML invoice template
    
    Args:
        student: Student object
        is_pending: Boolean indicating if this is a pending payment invoice
    """
    # Format date
    formatted_date = datetime.now().strftime("%d-%m-%Y")
    
    # Get or create StudentInvoice record for this student
    student_invoice, created = StudentInvoice.objects.get_or_create(student=student)
    
    # Get invoice settings for this CSR
    try:
        # First try to get invoice settings for the student's creator
        invoice_settings = InvoiceSettings.objects.get(csr=student.created_by)
        
        # Get the invoice number from the StudentInvoice model
        if is_pending:
            # For pending invoice, use P prefix with the stored pending invoice number
            if student_invoice.pending_invoice_no > 0:
                invoice_number = f"{student_invoice.pending_invoice_no}"
            else:
                # If no pending invoice number yet, use the current settings number
                invoice_number = f"{invoice_settings.current_serial_number}"
        else:
            # For regular invoice, use the stored present invoice number
            if student_invoice.present_invoice_no > 0:
                invoice_number = str(student_invoice.present_invoice_no)
            else:
                # If no present invoice number yet, use the current settings number
                invoice_number = str(invoice_settings.current_serial_number)
        
        # Get bank details from settings
        school_name = invoice_settings.school_name
        bank_name = invoice_settings.bank_name
        account_number = invoice_settings.account_number
        iban_number = invoice_settings.iban_number
    except InvoiceSettings.DoesNotExist:
        # If the student's creator doesn't have invoice settings, try to get from a Lead CSR
        try:
            # Find a Lead CSR with invoice settings
            lead_csr_settings = InvoiceSettings.objects.filter(csr__lead_role=True).first()
            
            if lead_csr_settings:
                invoice_settings = lead_csr_settings
                # Get the invoice number from the StudentInvoice model
                if is_pending:
                    # For pending invoice, use P prefix with the stored pending invoice number
                    if student_invoice.pending_invoice_no > 0:
                        invoice_number = f"{student_invoice.pending_invoice_no}"
                    else:
                        # If no pending invoice number yet, use the current settings number
                        invoice_number = f"{lead_csr_settings.current_serial_number}"
                else:
                    # For regular invoice, use the stored present invoice number
                    if student_invoice.present_invoice_no > 0:
                        invoice_number = str(student_invoice.present_invoice_no)
                    else:
                        # If no present invoice number yet, use the current settings number
                        invoice_number = str(lead_csr_settings.current_serial_number)
                school_name = invoice_settings.school_name
                bank_name = invoice_settings.bank_name
                account_number = invoice_settings.account_number
                iban_number = invoice_settings.iban_number
            else:
                # If no Lead CSR settings found, use defaults
                invoice_settings = None
                # Use student invoice numbers if available, otherwise use student ID
                if is_pending:
                    invoice_number = f"{student_invoice.pending_invoice_no}" if student_invoice.pending_invoice_no > 0 else f"P{student.id}"
                else:
                    invoice_number = str(student_invoice.present_invoice_no) if student_invoice.present_invoice_no > 0 else str(student.id)
                # Fallback to defaults
                school_name = "Arfa Karim Technology Incubator Pvt Ltd"
                bank_name = "JS Bank"
                account_number = "0002587773"
                iban_number = "PK56JSBL9561000002587773"
        except Exception:
            # Final fallback to defaults
            invoice_settings = None
            # Use student invoice numbers if available, otherwise use student ID
            if is_pending:
                invoice_number = f"P{student_invoice.pending_invoice_no}" if student_invoice.pending_invoice_no > 0 else f"P{student.id}"
            else:
                invoice_number = str(student_invoice.present_invoice_no) if student_invoice.present_invoice_no > 0 else str(student.id)
            school_name = "Arfa Karim Technology Incubator Pvt Ltd"
            bank_name = "JS Bank"
            account_number = "0002587773"
            iban_number = "PK56JSBL9561000002587773"
    
    # Format due date
    due_date = student.due_date.strftime('%d %b %Y') if student.due_date else 'N/A'
    
    # Get CSR name
    csr_name = student.get_creator_name()
    
    # Prepare context for template
    context = {
        'student': student,
        'formatted_date': formatted_date,
        'invoice_number': invoice_number,
        'school_name': school_name,
        'bank_name': bank_name,
        'account_number': account_number,
        'iban_number': iban_number,
        'due_date': due_date,
        'csr_name': csr_name
    }
    
    return context


def render_printable_invoice(request, student, is_pending=False):
    """Render HTML invoice for printing
    
    Args:
        request: HTTP request object
        student: Student object
        is_pending: Boolean indicating if this is a pending payment invoice
    """
    # Get context data for the invoice
    context = get_invoice_context(student, is_pending)
    
    # Add pending flag to context
    context['is_pending'] = is_pending
    
    # If pending invoice, set amount to balance and modify display values
    if is_pending:
        # For pending invoices, we show the balance amount instead of advance payment
        context['pending_amount'] = student.balance
        
        # Create a modified student object for the template
        # This avoids modifying the actual student record in the database
        from copy import copy
        modified_student = copy(student)
        
        # For pending invoices, we show balance as the payment amount
        # and set due amount to 0 (since it's being paid in full)
        modified_student.advance_payment = 0  # Don't show advance payment for pending invoices
        modified_student.balance = student.balance  # Show current balance
        modified_student.second_installment = student.balance  # Keep second_installment for backward compatibility
        
        # Update total_amount to include the balance payment
        modified_student.total_amount = student.advance_payment + student.balance
        
        # Replace the student in context with our modified version
        context['student'] = modified_student
    
    # Render the HTML template
    return render(request, 'invoice/printable_invoice.html', context)
