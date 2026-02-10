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
        # Idempotency check: If WhatsApp already sent, skip to avoid duplicates
        # Note: We rely on whatsapp_sent primarily for idempotency of the whole task
        if registration.whatsapp_sent:
            logger.info(f"[Task] send_registration_confirmation: WhatsApp already sent for registration {registration_id}. Skipping.")
            return
        
        # 1. Send WhatsApp notification (primary requirement)
        logger.info(f"[Task] send_registration_confirmation: Sending WhatsApp to {registration.full_name} ({registration.phone_number})")
        whatsapp_ok = send_whatsapp_message_for_registration(registration)

        # Handle Meta sandbox: do not retry if recipient not whitelisted
        if whatsapp_ok == "SANDBOX":
            logger.warning(f"[Task] send_registration_confirmation: Meta sandbox - recipient not allowed for registration {registration_id}. Skipping retries.")
            return

        if whatsapp_ok:
            # Mark as sent in DB to prevent duplicates
            registration.whatsapp_sent = True
            registration.save(update_fields=['whatsapp_sent'])
            logger.info(f"[Task] send_registration_confirmation: WhatsApp sent successfully for registration {registration_id}")
        else:
            # WhatsApp failed - log and retry
            logger.warning(f"[Task] send_registration_confirmation: WhatsApp failed for registration {registration_id}. Retrying...")
            # Celery will retry this task up to max_retries times
            raise self.retry(exc=Exception("WhatsApp delivery failed"), countdown=60)
        
        # 2. Send email notification (secondary - don't retry task if only email fails)
        try:
            logger.info(f"[Task] send_registration_confirmation: Sending confirmation email to {registration.email}")
            email_ok = send_registration_email(registration)
            if email_ok:
                logger.info(f"[Task] send_registration_confirmation: Email sent successfully for registration {registration_id}")
            else:
                logger.warning(f"[Task] send_registration_confirmation: Email send returned False for registration {registration_id}")
        except Exception as email_e:
            # Email failure should NOT cause task retry - just log and continue
            logger.error(f"[Task] send_registration_confirmation: Exception while sending email for registration {registration_id}: {str(email_e)}")
            # Don't raise - email is secondary

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
        
        # Idempotency check: If already sent, skip to prevent duplicate WhatsApp messages
        if assignment.allotment_notification_sent:
            logger.info(f"[Task] send_duty_allotment_notification: Message already sent for duty {duty_assignment_id}. Skipping.")
            return
        
        # 1. Send WhatsApp notification
        logger.info(f"[Task] send_duty_allotment_notification: Sending WhatsApp to {user.full_name} ({user.phone_number}) for duty on {assignment.duty_date}")
        ok = send_whatsapp_message_for_allotment(assignment)

        # If Meta sandbox causes skip, do not retry
        if ok == "SANDBOX":
            logger.warning(f"[Task] send_duty_allotment_notification: Meta sandbox - recipient not allowed for duty {duty_assignment_id}. Skipping retries.")
            return

        if ok:
            # Mark as sent to prevent duplicates on subsequent signal triggers
            assignment.allotment_notification_sent = True
            assignment.save(update_fields=['allotment_notification_sent'])
            logger.info(f"[Task] send_duty_allotment_notification: WhatsApp sent successfully for duty {duty_assignment_id}")
        else:
            # WhatsApp failed - log and retry
            logger.warning(f"[Task] send_duty_allotment_notification: WhatsApp failed for duty {duty_assignment_id}. Retrying...")
            raise self.retry(exc=Exception(f"WhatsApp delivery failed for duty {duty_assignment_id}"), countdown=60)

        # 2. Send Email notification (secondary)
        try:
            logger.info(f"[Task] send_duty_allotment_notification: Sending allotment email to {user.email}")
            email_ok = send_allotment_email(assignment)
            if email_ok:
                logger.info(f"[Task] send_duty_allotment_notification: Email sent successfully for duty {duty_assignment_id}")
            else:
                logger.warning(f"[Task] send_duty_allotment_notification: Email send returned False for duty {duty_assignment_id}")
        except Exception as email_e:
            logger.error(f"[Task] send_duty_allotment_notification: Exception while sending email for duty {duty_assignment_id}: {str(email_e)}")

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
