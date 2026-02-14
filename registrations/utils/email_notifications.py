"""
Email Notification Service.
Mirrors the WhatsApp notification flow for Registration, Allotment, and Reminders.
"""

import logging
from django.conf import settings
from django.core.mail import send_mail

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
    Subject: "Registration Received – Madras Jamaat Portal"
    Body variables:
    - Full Name
    """
    subject = "Registration Received – Madras Jamaat Portal"
    
    body = f"""Assalamu Alaikum {registration.full_name},

We have received your registration for requests.

JazakAllah Khair,
Jamaat Administration
"""
    return send_email(registration.email, subject, body)

def send_allotment_email(duty_assignment):
    """
    Trigger: Admin allots duty
    Subject: "Duty Allotment Confirmed – Madras Jamaat Portal"
    Body variables:
    - Full Name
    - Date
    - Time
    """
    user = duty_assignment.assigned_user
    
    # Format Date: 12 March 2026
    date_str = duty_assignment.duty_date.strftime('%d %B %Y')
    
    # Determine time label
    time_str = "N/A"
    if hasattr(duty_assignment, 'slot') and duty_assignment.slot:
        time_str = duty_assignment.slot.time_label
    else:
        time_str = duty_assignment.get_namaaz_type_display()

    subject = "Duty Allotment Confirmed – Madras Jamaat Portal"
    
    body = f"""Assalamu Alaikum {user.full_name},

You have been allotted the following duty:
Date: {date_str}
Time: {time_str}

Please be present on time.

JazakAllah Khair,
Jamaat Administration
"""
    return send_email(user.email, subject, body)

def send_reminder_email(registration, date_str, time_str):
    """
    Trigger: 24 hours before scheduled duty/event
    Subject: "Reminder – Duty Tomorrow"
    Body variables:
    - Full Name
    - Date
    - Time
    """
    subject = "Reminder – Duty Tomorrow"
    
    body = f"""Assalamu Alaikum {registration.full_name},

This is a reminder for your duty tomorrow:
Date: {date_str}
Time: {time_str}

Please ensure you arrive on time.

JazakAllah Khair,
Jamaat Administration
"""
    return send_email(registration.email, subject, body)
