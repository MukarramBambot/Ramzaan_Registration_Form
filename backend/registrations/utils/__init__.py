"""
Reminder utilities for automatic email and WhatsApp sending.
Handles scheduling, sending, and tracking of duty reminders.
"""

from datetime import datetime, timedelta
import threading
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
import pytz
import requests
import logging

from ..models import Reminder, ReminderLog, DutyAssignment
from .whatsapp import (
    send_registration_received, 
    send_duty_allotment,
    send_duty_reminder_tomorrow,
    send_correction_req_v1,
    send_correction_done_v1
)
from .reporting import get_reporting_time

logger = logging.getLogger(__name__)

def send_confirmation_email(registration):
    """
    Sends a confirmation email to the user after registration.
    """
    try:
        subject = "Registration Received - Sherullah Azaan & Takbira"
        message = (
            f"Assalamu Alaikum {registration.full_name},\n\n"
            f"We have received your registration for Sherullah 1447 Azaan & Takbira duties.\n"
            f"ITS Number: {registration.its_number}\n\n"
            f"You will be notified once the duties are allotted.\n\n"
            f"JazakAllah Khair,\n"
            f"Jamaat Administration"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[registration.email],
            fail_silently=False
        )
        return True
    except Exception as e:
        logger.error(f"Email Error: Failed to send confirmation to {registration.email}: {str(e)}")
        return False

def send_whatsapp_message_for_registration(registration):
    """
    Wrapper for registration WhatsApp notification.
    Returns full result dict from whatsapp.py
    """
    return send_registration_received(
        phone=registration.phone_number,
        full_name=registration.full_name
    )

def send_whatsapp_message_for_allotment(duty_assignment):
    """
    Wrapper for duty allotment WhatsApp notification.
    """
    # Extract details
    user = duty_assignment.assigned_user
    date_str = duty_assignment.duty_date.strftime("%d %B %Y")
    
    # Extract time label
    if hasattr(duty_assignment, "slot") and duty_assignment.slot:
        time_str = duty_assignment.slot.time_label
    else:
        time_str = duty_assignment.get_namaaz_type_display()

    reporting_time = get_reporting_time(duty_assignment)

    return send_duty_allotment(
        phone=user.phone_number,
        full_name=user.full_name,
        duty_date=date_str,
        duty_time=time_str,
        reporting_time=reporting_time
    )

# Timezone configuration
IST = pytz.timezone('Asia/Kolkata')

# Reminder configuration
REMINDER_TIME_HOUR = getattr(settings, 'REMINDER_TIME_HOUR', 18)  # Default: 6 PM
REMINDER_TIME_MINUTE = getattr(settings, 'REMINDER_TIME_MINUTE', 0)
MAX_RETRY_ATTEMPTS = 2


def calculate_reminder_datetime(duty_date):
    """
    Calculate when reminder should be sent.
    ONE DAY BEFORE at configured time (default 6 PM IST).
    """
    # Reminder date = duty_date - 1 day
    reminder_date = duty_date - timedelta(days=1)
    
    # Create datetime at configured time in IST
    naive_dt = datetime.combine(
        reminder_date,
        datetime.min.time().replace(
            hour=REMINDER_TIME_HOUR,
            minute=REMINDER_TIME_MINUTE
        )
    )
    
    # Make timezone-aware
    aware_dt = IST.localize(naive_dt)
    
    return aware_dt


def create_reminder_for_assignment(duty_assignment):
    """
    Create a reminder for a newly created duty assignment.
    Called automatically when duty is assigned.
    
    Args:
        duty_assignment: DutyAssignment instance
    
    Returns:
        Reminder instance or None
    """
    try:
        # Cancel any existing reminder for this assignment (in case of reassignment)
        Reminder.objects.filter(duty_assignment=duty_assignment).update(status='CANCELLED')
        
        # Calculate when to send reminder
        scheduled_dt = calculate_reminder_datetime(duty_assignment.duty_date)
        
        # Create new reminder
        reminder = Reminder.objects.create(
            duty_assignment=duty_assignment,
            scheduled_datetime=scheduled_dt,
            status='PENDING'
        )
        
        logger.info(f"Created reminder {reminder.id} for {duty_assignment}, scheduled at {scheduled_dt}")
        return reminder
        
    except Exception as e:
        logger.error(f"Failed to create reminder for {duty_assignment}: {str(e)}")
        return None





def cancel_reminders_for_assignment(duty_assignment):
    """
    Cancel reminders when duty is unlocked/changed.
    
    Args:
        duty_assignment: DutyAssignment instance
    """
    try:
        cancelled_count = Reminder.objects.filter(
            duty_assignment=duty_assignment,
            status='PENDING'
        ).update(status='CANCELLED')
        
        logger.info(f"Cancelled {cancelled_count} reminders for {duty_assignment}")
        
    except Exception as e:
        logger.error(f"Failed to cancel reminders for {duty_assignment}: {str(e)}")


def send_email_reminder(reminder):
    """
    Send email reminder for a duty assignment.
    Uses centralized email_notifications service.
    
    Args:
        reminder: Reminder instance
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        duty = reminder.duty_assignment
        user = duty.assigned_user
        
        # Format Date: 12 March 2026
        date_str = duty.duty_date.strftime('%d %B %Y')
        
        # Determine time label
        time_str = "N/A"
        if hasattr(duty, 'slot') and duty.slot:
            time_str = duty.slot.time_label
        else:
            time_str = duty.get_namaaz_type_display()

        # Call new service
        from .email_notifications import send_reminder_email
        reporting_time = get_reporting_time(duty)
        email_ok = send_reminder_email(user, date_str, time_str, reporting_time)
        
        if email_ok:
            # Update reminder
            reminder.email_sent = True
            reminder.email_attempts += 1
            reminder.save()
            
            # Log success
            ReminderLog.objects.create(
                reminder=reminder,
                channel='EMAIL',
                success=True,
                message=f"Email sent to {user.email}"
            )
            return True
        else:
            raise Exception("Email service returned False")
        
    except Exception as e:
        error_msg = f"Email send failed: {str(e)}"
        logger.error(f"Reminder {reminder.id} - {error_msg}")
        
        reminder.email_attempts += 1
        reminder.last_error = error_msg
        reminder.save()
        
        # Log failure
        ReminderLog.objects.create(
            reminder=reminder,
            channel='EMAIL',
            success=False,
            message=error_msg
        )
        
        return False


def send_whatsapp_reminder(reminder):
    """
    Send WhatsApp reminder using official WhatsApp Business API.
    
    Uses a pre-approved utility template for duty reminders.
    
    Args:
        reminder: Reminder instance
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        duty = reminder.duty_assignment
        user = duty.assigned_user
        
        # Use consolidated utility
        from .whatsapp import send_duty_reminder_tomorrow
        
        # Format Date and Time
        date_str = duty.duty_date.strftime('%d %B %Y')
        
        # Determine time label
        time_label = "N/A"
        if hasattr(duty, 'slot') and duty.slot:
            time_label = duty.slot.time_label
        else:
            time_label = duty.get_namaaz_type_display()

        # The new function expects (phone, name, date, time, reporting_time)
        reporting_time = get_reporting_time(duty)
        result = send_duty_reminder_tomorrow(
            phone=user.phone_number,
            full_name=user.full_name,
            duty_date=date_str,
            duty_time=time_label,
            reporting_time=reporting_time
        )
        
        success = result.get('success', False)
        
        # Save metadata regardless of success
        reminder.whatsapp_message_id = result.get('message_id')
        reminder.whatsapp_status = 'SENT' if success else 'FAILED'
        if success:
             reminder.whatsapp_sent = True
             reminder.whatsapp_attempts += 1
             reminder.sent_at = timezone.now()
             # Clear previous errors on success
             reminder.last_error = ""
        else:
             # Extract error
             error_data = result.get('response', {}).get('error', {})
             error_msg = str(error_data) if isinstance(error_data, dict) else str(result.get('response'))
             reminder.whatsapp_attempts += 1
             reminder.last_error = error_msg
        
        reminder.save()
        
        if success:
            # Log success
            ReminderLog.objects.create(
                reminder=reminder,
                channel='WHATSAPP',
                success=True,
                message=f"WhatsApp sent via template to {user.phone_number} (ID: {reminder.whatsapp_message_id})"
            )
            return True
        else:
            raise Exception(f"Template delivery failed: {reminder.last_error}")
            
    except Exception as e:
        error_msg = f"WhatsApp reminder failed: {str(e)}"
        logger.error(f"Reminder {reminder.id} - {error_msg}")
        
        reminder.whatsapp_attempts += 1
        reminder.last_error = error_msg
        reminder.save()
        
        # Log failure
        ReminderLog.objects.create(
            reminder=reminder,
            channel='WHATSAPP',
            success=False,
            message=error_msg
        )
        
        return False
        
    except Exception as e:
        error_msg = f"WhatsApp send failed: {str(e)}"
        logger.error(f"Reminder {reminder.id} - {error_msg}")
        
        reminder.whatsapp_attempts += 1
        reminder.last_error = error_msg
        reminder.save()
        
        # Log failure
        ReminderLog.objects.create(
            reminder=reminder,
            channel='WHATSAPP',
            success=False,
            message=error_msg
        )
        
        return False


def process_pending_reminders():
    """
    Process all pending reminders that are due.
    Called by Celery beat task periodically.
    
    Returns:
        dict: Summary of processed reminders
    """
    now = timezone.now()
    
    # Find all pending reminders that are due
    due_reminders = Reminder.objects.filter(
        status='PENDING',
        scheduled_datetime__lte=now
    ).select_related('duty_assignment', 'duty_assignment__assigned_user')
    
    stats = {
        'total_due': due_reminders.count(),
        'email_success': 0,
        'email_failed': 0,
        'whatsapp_success': 0,
        'whatsapp_failed': 0,
        'completed': 0,
        'failed': 0
    }
    
    logger.info(f"Processing {stats['total_due']} due reminders...")
    
    for reminder in due_reminders:
        email_ok = False
        whatsapp_ok = False
        
        # Send email (if not already sent)
        if not reminder.email_sent and reminder.email_attempts < MAX_RETRY_ATTEMPTS:
            email_ok = send_email_reminder(reminder)
            if email_ok:
                stats['email_success'] += 1
            else:
                stats['email_failed'] += 1
        elif reminder.email_sent:
            email_ok = True
        
        # Send WhatsApp (if not already sent)
        if not reminder.whatsapp_sent and reminder.whatsapp_attempts < MAX_RETRY_ATTEMPTS:
            whatsapp_ok = send_whatsapp_reminder(reminder)
            if whatsapp_ok:
                stats['whatsapp_success'] += 1
            else:
                stats['whatsapp_failed'] += 1
        elif reminder.whatsapp_sent:
            whatsapp_ok = True
        
        # Update reminder status
        if email_ok and whatsapp_ok:
            reminder.mark_sent()
            stats['completed'] += 1
        elif reminder.email_attempts >= MAX_RETRY_ATTEMPTS and reminder.whatsapp_attempts >= MAX_RETRY_ATTEMPTS:
            reminder.mark_failed("Max retry attempts reached")
            stats['failed'] += 1
    
    logger.info(f"Reminder processing complete: {stats}")
    return stats


def safe_task_delay(task_func, *args, **kwargs):
    """
    Safely triggers a Celery task or falls back to synchronous execution.
    PASS ONLY PRIMITIVE DATA (int, str) to args/kwargs.
    """
    from django.conf import settings
    import threading
    
    non_blocking = kwargs.pop('non_blocking', False)
    celery_enabled = getattr(settings, 'CELERY_ENABLED', True)
    
    # Extract only serializable args/kwargs for the thread closure
    # This is a fail-safe to prevent capturing outer scope objects
    task_args = list(args)
    task_kwargs = dict(kwargs)

    def _execute():
        try:
            if celery_enabled and hasattr(task_func, 'delay'):
                try:
                    task_func.delay(*task_args, **task_kwargs)
                    logger.info(f"Task {task_func.__name__} enqueued successfully.")
                    return
                except Exception as celery_e:
                    logger.warning(f"Celery failed for {task_func.__name__}, falling back: {str(celery_e)}")
            
            # Fallback (Synchronous or Threaded)
            if hasattr(task_func, 'run'):
                task_func.run(*task_args, **task_kwargs)
            else:
                task_func(*task_args, **task_kwargs)
            logger.info(f"Task {task_func.__name__} executed in fallback mode.")
        except Exception as e:
            logger.error(f"Task {task_func.__name__} failed in execution: {str(e)}")

    if non_blocking:
        t = threading.Thread(target=_execute)
        t.daemon = True
        t.start()
        return "THREADED"
    else:
        return _execute()
