"""
Email Notification Service.
Mirrors the WhatsApp notification flow for Registration, Allotment, and Reminders.
"""

import logging
from django.conf import settings
from django.core.mail import send_mail

from .reporting import get_reporting_time

logger = logging.getLogger('registrations')

def send_email(to_email, subject, message):
    """
    Wrapper for Django send_mail with logging and error handling.
    """
    if not to_email:
        logger.warning("[Email] No recipient email provided. Skipping.")
        return False

    try:
        logger.info(f"[Email] Sending '{subject}' to {to_email}")
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            fail_silently=False
        )
        logger.info(f"[Email] ✓ SUCCESS to {to_email}")
        return True
    except Exception as e:
        logger.error(f"[Email] Failed to send to {to_email}: {str(e)}")
        return False

def send_registration_email(registration):
    """
    Trigger: User submits the registration form
    Subject: "Sherullah Registration Received"
    """
    subject = "Sherullah Registration Received"
    
    applied_khidmat = registration.get_preference_display()
    
    body = f"""Afzalus salam {registration.full_name},

Your Sherullah registration has been received successfully.

You have applied for the following khidmat:
{applied_khidmat}

Our team will review your application and notify you once duty is allotted.

JazakAllah Khair,
Jamaat Administration
"""
    return send_email(registration.email, subject, body)

def send_allotment_email(duty_assignment):
    """
    Trigger: Admin allots duty
    Subject: "Sherullah Duty Allotment Confirmation"
    """
    user = duty_assignment.assigned_user
    
    # Format Date: 12 March 2026
    date_str = duty_assignment.duty_date.strftime('%d %B %Y')
    
    # Determine duty name
    if hasattr(duty_assignment, 'slot') and duty_assignment.slot:
        duty_name = duty_assignment.slot.time_label
    else:
        duty_name = duty_assignment.get_namaaz_type_display()

    subject = "Sherullah Duty Allotment Confirmation"
    
    reporting_time = get_reporting_time(duty_assignment) or "N/A"
    
    body = f"""Afzalus salam {user.full_name},

You have been allotted the following khidmat:

Date: {date_str}
Khidmat: {duty_name}
Reporting Time: {reporting_time}

This allotment is non-transferable. Please ensure you are present at the mosque on time.

JazakAllah Khair,
Jamaat Administration
"""
    return send_email(user.email, subject, body)

def send_reminder_email(user, date_str, duty_name, reporting_time=None):
    """
    Trigger: 24 hours before scheduled duty/event
    Subject: "Reminder: Sherullah Khidmat Tomorrow"
    """
    subject = "Reminder: Sherullah Khidmat Tomorrow"
    
    reporting_str = reporting_time if reporting_time else "N/A"
    
    body = f"""Afzalus salam {user.full_name},

This is a reminder for your Sherullah khidmat tomorrow.

Date: {date_str}
Khidmat: {duty_name}
Reporting Time: {reporting_str}

Please ensure you arrive at the mosque on time.

JazakAllah Khair,
Jamaat Administration
"""
    return send_email(user.email, subject, body)

def send_correction_email(correction):
    """
    Trigger: Admin requests a correction
    Subject: "Action Required: Sherullah Registration Correction"
    """
    registration = correction.registration
    base_url = "https://madrasjamaatportal.org" 
    link = f"{base_url}/correction.php?token={correction.token}"
    
    subject = "Action Required: Sherullah Registration Correction"
    
    field_display = correction.field_name.replace('_', ' ').title()
    
    body = f"""Afzalus salam {registration.full_name},

Your Sherullah registration requires correction.

Field: {field_display}

Message:
{correction.admin_message}

Please update your details using the link below:
{link}

JazakAllah Khair,
Jamaat Administration
"""
    return send_email(registration.email, subject, body)

def send_correction_completed_email(registration):
    """
    Trigger: User resolves a correction
    Subject: "Sherullah Correction Received"
    """
    subject = "Sherullah Correction Received"
    
    body = f"""Afzalus salam {registration.full_name},

Your correction has been received successfully.

Our team will review the updated information shortly.

JazakAllah Khair,
Jamaat Administration
"""
    return send_email(registration.email, subject, body)
