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
        whatsapp_ok = send_whatsapp_message_for_registration(registration)

        if whatsapp_ok == "SANDBOX": return
        if whatsapp_ok:
            registration.whatsapp_sent = True
            registration.save(update_fields=['whatsapp_sent'])
        else:
            # Handle retry if in Celery, otherwise just log
            if hasattr(self, 'retry') and self is not None:
                raise self.retry(exc=Exception("WhatsApp delivery failed"), countdown=60)
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
        ok = send_whatsapp_message_for_allotment(assignment)

        if ok == "SANDBOX": return
        if ok:
            assignment.allotment_notification_sent = True
            assignment.save(update_fields=['allotment_notification_sent'])
        else:
            if hasattr(self, 'retry') and self is not None:
                raise self.retry(exc=Exception("WhatsApp failed"), countdown=60)
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
