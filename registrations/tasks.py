"""
Celery tasks for automated reminder processing.
These tasks run in the background on a schedule.
"""

from celery import shared_task
from django.utils import timezone
import logging

from .utils import process_pending_reminders
from .google_sheets import sync_registration_to_sheets

logger = logging.getLogger(__name__)


@shared_task(name='registrations.notify_admin_cancel_request', bind=True)
def notify_admin_cancel_request_task(self, duty_assignment_id):
    """
    Notify admin via WhatsApp about a cancellation request.
    """
    from .models import DutyAssignment
    from .utils.whatsapp import send_admin_text_message
    from django.conf import settings

    logger.info(f"[Task] notify_admin_cancel_request: Starting for duty_assignment_id={duty_assignment_id}")
    try:
        assignment = DutyAssignment.objects.select_related('assigned_user').get(id=duty_assignment_id)
    except DutyAssignment.DoesNotExist:
        logger.error(f"[Task] notify_admin_cancel_request: DutyAssignment {duty_assignment_id} not found. Aborting.")
        return

    admin_phone = getattr(settings, 'ADMIN_WHATSAPP_NUMBER', None)
    if not admin_phone:
        logger.error("[Task] notify_admin_cancel_request: ADMIN_WHATSAPP_NUMBER not configured in settings.")
        return

    user = assignment.assigned_user
    date_str = assignment.duty_date.strftime('%d %B %Y')
    khidmat = assignment.get_namaaz_type_display()
    reason = assignment.cancel_reason or 'No reason provided.'

    message = (
        f"Khidmat Cancellation Request\n\n"
        f"Name: {user.full_name}\n"
        f"ITS: {user.its_number}\n"
        f"Date: {date_str}\n"
        f"Khidmat: {khidmat}\n\n"
        f"Reason: {reason}"
    )

    result = send_admin_text_message(admin_phone, message)
    logger.info(f"[Task] notify_admin_cancel_request: Completed for {duty_assignment_id} -> {result.get('success')}")


@shared_task(name='registrations.notify_admin_reallocation_request', bind=True)
def notify_admin_reallocation_request_task(self, duty_assignment_id):
    """
    Notify admin via WhatsApp about a reallocation request.
    """
    from .models import DutyAssignment
    from .utils.whatsapp import send_admin_text_message
    from django.conf import settings

    logger.info(f"[Task] notify_admin_reallocation_request: Starting for duty_assignment_id={duty_assignment_id}")
    try:
        assignment = DutyAssignment.objects.select_related('assigned_user').get(id=duty_assignment_id)
    except DutyAssignment.DoesNotExist:
        logger.error(f"[Task] notify_admin_reallocation_request: DutyAssignment {duty_assignment_id} not found. Aborting.")
        return

    admin_phone = getattr(settings, 'ADMIN_WHATSAPP_NUMBER', None)
    if not admin_phone:
        logger.error("[Task] notify_admin_reallocation_request: ADMIN_WHATSAPP_NUMBER not configured in settings.")
        return

    user = assignment.assigned_user
    date_str = assignment.duty_date.strftime('%d %B %Y')
    khidmat = assignment.get_namaaz_type_display()
    reason = assignment.reallocation_reason or 'No reason provided.'

    message = (
        f"Khidmat Reallocation Request\n\n"
        f"Name: {user.full_name}\n"
        f"ITS: {user.its_number}\n"
        f"Current Date: {date_str}\n"
        f"Khidmat: {khidmat}\n\n"
        f"Reason: {reason}"
    )

    result = send_admin_text_message(admin_phone, message)
    logger.info(f"[Task] notify_admin_reallocation_request: Completed for {duty_assignment_id} -> {result.get('success')}")


@shared_task(
    name='registrations.sync_to_sheets',
    bind=True,
    max_retries=5,
    default_retry_delay=300 # 5 minutes between retries
)
def sync_to_sheets_task(self, registration_id):
    """
    Background task to sync a new registration to Google Sheets.
    """
    from .models import Registration
    try:
        registration = Registration.objects.get(id=registration_id)
        sync_registration_to_sheets(registration)
    except Registration.DoesNotExist:
        logger.error(f"Sync failed: Registration {registration_id} not found")
    except Exception as e:
        logger.error(f"Sync task failed for {registration_id}: {str(e)}")
        raise self.retry(exc=e)


@shared_task(name='registrations.process_reminders')
def process_reminders_task():
    """
    Celery task to process pending reminders.
    Runs periodically (every 15 minutes recommended).
    
    Returns:
        dict: Processing statistics
    """
    try:
        logger.info("Starting reminder processing task...")
        stats = process_pending_reminders()
        logger.info(f"Reminder processing task completed: {stats}")
        return stats
    except Exception as e:
        logger.error(f"Reminder processing task failed: {str(e)}")
        raise


@shared_task(name='registrations.cleanup_old_reminders')
def cleanup_old_reminders():
    """
    Cleanup task to archive old sent/failed reminders.
    Runs daily to keep database clean.
    
    Keeps reminders for 90 days after sending.
    """
    from datetime import timedelta
    from .models import Reminder
    
    try:
        cutoff_date = timezone.now() - timedelta(days=90)
        
        deleted_count, _ = Reminder.objects.filter(
            status__in=['SENT', 'FAILED', 'CANCELLED'],
            sent_at__lt=cutoff_date
        ).delete()
        
        logger.info(f"Cleaned up {deleted_count} old reminders")
        return {'deleted': deleted_count}
        
    except Exception as e:
        logger.error(f"Cleanup task failed: {str(e)}")
        raise


@shared_task(
    name='registrations.send_registration_confirmation',
    bind=True,
    max_retries=3,
    default_retry_delay=60  # Retry after 1 minute on failure
)
def send_registration_confirmation_task(self, registration_id):
    """
    Send WhatsApp + Email confirmation notification for a new registration.
    Runs as async Celery task to NOT block API response.
    
    Idempotency: Checks whatsapp_sent flag to avoid duplicate messages.
    Failure Handling: WhatsApp failure is logged+retried; Email failure does not block.
    """
    from .models import Registration
    from .utils import send_whatsapp_message_for_registration
    from .utils.email_notifications import send_registration_email

    logger.info(f"[Task] send_registration_confirmation: Starting for registration_id={registration_id}")
    
    try:
        registration = Registration.objects.get(id=registration_id)
    except Registration.DoesNotExist:
        logger.error(f"[Task] send_registration_confirmation: Registration {registration_id} not found. Aborting.")
        return  # Don't retry if record doesn't exist
    
    try:
        # 1. Send email notification (Independent step)
        try:
            logger.info(f"[Task] send_registration_confirmation: Sending confirmation email to {registration.email}")
            send_registration_email(registration)
            logger.info(f"[Task] send_registration_confirmation: Email attempted for {registration_id}")
        except Exception as email_e:
            logger.error(f"[Task] send_registration_confirmation: Email failed for {registration_id}: {str(email_e)}")

        # 2. Idempotency check for WhatsApp
        if registration.whatsapp_sent:
            return
        
        # 3. Send WhatsApp notification
        logger.info(f"[Task] send_registration_confirmation: Sending WhatsApp to {registration.phone_number}")
        result = send_whatsapp_message_for_registration(registration)
        
        success = result.get('success', False)
        
        # Save metadata
        registration.whatsapp_message_id = result.get('message_id')
        registration.whatsapp_status = 'SENT' if success else 'FAILED'
        
        if success:
            registration.whatsapp_sent = True
            registration.whatsapp_error = "" # clear error
            registration.save(update_fields=['whatsapp_sent', 'whatsapp_message_id', 'whatsapp_status', 'whatsapp_error'])
        else:
            error_data = result.get('response', {}).get('error', {})
            registration.whatsapp_error = str(error_data)
            registration.save(update_fields=['whatsapp_message_id', 'whatsapp_status', 'whatsapp_error'])
            
            # Handle retry if in Celery, otherwise just log
            if hasattr(self, 'retry') and self is not None:
                raise self.retry(exc=Exception(f"WhatsApp delivery failed: {registration.whatsapp_error}"), countdown=60)
            logger.warning(f"[Task] send_registration_confirmation: WhatsApp failed (no retry possible).")

    except Exception as exc:
        if isinstance(exc, self.MaxRetriesExceededError if hasattr(self, 'MaxRetriesExceededError') else Exception):
             logger.error(f"Max retries or fatal error: {str(exc)}")
        else:
             raise

    except self.MaxRetriesExceededError:
        logger.error(f"[Task] send_registration_confirmation: Max retries exceeded for registration {registration_id}")
        # Mark as failed but don't crash
        registration.whatsapp_sent = False
        registration.save(update_fields=['whatsapp_sent'])
    except Exception as exc:
        # Unexpected error - log and retry if retries remain
        logger.error(f"[Task] send_registration_confirmation: Unexpected error for registration {registration_id}: {str(exc)}")
        if not isinstance(exc, Registration.DoesNotExist):
            raise self.retry(exc=exc, countdown=60)
    
    logger.info(f"[Task] send_registration_confirmation: Completed for registration_id={registration_id}")


@shared_task(
    name='registrations.send_duty_allotment_notification',
    bind=True,
    max_retries=3,
    default_retry_delay=60  # Retry after 1 minute on failure
)
def send_duty_allotment_notification_task(self, duty_assignment_id):
    """
    Send WhatsApp + Email notification when duty is assigned to a user.
    Runs as async Celery task to NOT block API response.
    
    Idempotency: Checks allotment_notification_sent flag to prevent duplicate messages.
    Prevents re-sending on admin edits or trigger misfires.
    """
    from .models import DutyAssignment
    from .utils import send_whatsapp_message_for_allotment
    from .utils.email_notifications import send_allotment_email

    logger.info(f"[Task] send_duty_allotment_notification: Starting for duty_assignment_id={duty_assignment_id}")
    
    try:
        assignment = DutyAssignment.objects.select_related('assigned_user').get(id=duty_assignment_id)
    except DutyAssignment.DoesNotExist:
        logger.error(f"[Task] send_duty_allotment_notification: DutyAssignment {duty_assignment_id} not found. Aborting.")
        return  # Don't retry if record doesn't exist
    
    try:
        user = assignment.assigned_user
        
        # 1. Send Email notification (Independent step)
        try:
            logger.info(f"[Task] send_duty_allotment_notification: Sending allotment email to {user.email}")
            send_allotment_email(assignment)
        except Exception as email_e:
            logger.error(f"[Task] send_duty_allotment_notification: Email failed: {str(email_e)}")

        # 2. Idempotency check for WhatsApp
        if assignment.allotment_notification_sent:
            return
        
        # 3. Send WhatsApp notification
        logger.info(f"[Task] send_duty_allotment_notification: Sending WhatsApp to {user.phone_number}")
        result = send_whatsapp_message_for_allotment(assignment)
        
        success = result.get('success', False)

        if success:
            assignment.allotment_notification_sent = True
            assignment.save(update_fields=['allotment_notification_sent'])
            logger.info(f"[Task] WhatsApp sent to {user.phone_number} (ID: {result.get('message_id')})")
        else:
            error_msg = result.get('response', {}).get('error', "Unknown Error")
            if hasattr(self, 'retry') and self is not None:
                raise self.retry(exc=Exception(f"WhatsApp failed: {error_msg}"), countdown=60)
            logger.warning(f"[Task] send_duty_allotment_notification: WhatsApp failed (no retry possible).")

    except Exception as exc:
        # Avoid crashing background thread on Celery specific errors when running in-process
        if 'Retry' in str(type(exc)): raise
        logger.error(f"Task fatal error: {str(exc)}")
        if not isinstance(exc, DutyAssignment.DoesNotExist) and hasattr(self, 'retry'):
            raise self.retry(exc=exc, countdown=60)

    except self.MaxRetriesExceededError:
        logger.error(f"[Task] send_duty_allotment_notification: Max retries exceeded for duty {duty_assignment_id}. Giving up.")
        # Mark as failed in DB but don't crash
        assignment.allotment_notification_sent = False
        assignment.save(update_fields=['allotment_notification_sent'])
    except Exception as exc:
        # Unexpected error - log and retry if retries remain
        logger.error(f"[Task] send_duty_allotment_notification: Unexpected error for duty {duty_assignment_id}: {str(exc)}")
        if not isinstance(exc, DutyAssignment.DoesNotExist):
            raise self.retry(exc=exc, countdown=60)
    
    logger.info(f"[Task] send_duty_allotment_notification: Completed for duty_assignment_id={duty_assignment_id}")
