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
        logger.info("[Celery] Starting reminder processing task...")
        # We wrap the utility call to ensure task-level reporting
        stats = process_pending_reminders()
        logger.info(f"[Celery] Reminder processing completed: {stats}")
        return stats
    except Exception as e:
        logger.critical(f"[Celery] CRITICAL FAILURE in reminder task: {str(e)}")
        # We still raise if it's a transient infrastructure issue, 
        # but the business logic errors are caught in the loop inside process_pending_reminders.
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


@shared_task(
    name='registrations.send_correction_notification',
    bind=True,
    max_retries=3,
    default_retry_delay=60
)
def send_correction_notification_task(self, correction_id):
    """
    Send WhatsApp + Email notification when a correction is requested.
    """
    from .models import RegistrationCorrection
    from .utils.whatsapp import send_correction_notification
    from .utils.email_notifications import send_correction_email

    logger.info(f"[Task] send_correction_notification: Starting for correction_id={correction_id}")
    
    try:
        correction = RegistrationCorrection.objects.select_related('registration').get(id=correction_id)
    except RegistrationCorrection.DoesNotExist:
        logger.error(f"[Task] send_correction_notification: Correction {correction_id} not found.")
        return

    try:
        # 1. Email notification (Independent)
        try:
            logger.info(f"[Task] send_correction_notification: Sending email for {correction_id}")
            send_correction_email(correction)
        except Exception as e:
            logger.error(f"[Task] send_correction_notification: Email failed: {str(e)}")

        # 2. WhatsApp notification
        logger.info(f"[Task] send_correction_notification: Sending WhatsApp for {correction_id}")
        result = send_correction_notification(correction)
        
        if result.get('success'):
            logger.info(f"[Task] send_correction_notification: ✓ WhatsApp sent for {correction_id}")
        else:
            error_msg = result.get('response', {}).get('error', 'Unknown WhatsApp error')
            logger.error(f"[Task] send_correction_notification: ❌ WhatsApp failed: {error_msg}")
            if hasattr(self, 'retry'):
                raise self.retry(exc=Exception(error_msg), countdown=60)

    except Exception as exc:
        if 'Retry' in str(type(exc)): raise
        logger.error(f"Task fatal error: {str(exc)}")
        if hasattr(self, 'retry'):
            raise self.retry(exc=exc, countdown=60)

@shared_task(
    name='registrations.send_correction_completed_notification',
    bind=True,
    max_retries=3,
    default_retry_delay=60
)
def send_correction_completed_notification_task(self, registration_id):
    """
    Send WhatsApp + Email notification when a correction is resolved.
    """
    from .models import Registration
    from .utils.whatsapp import send_correction_done_v1
    from .utils.email_notifications import send_correction_completed_email

    logger.info(f"[Task] send_correction_completed_notification: Starting for registration_id={registration_id}")
    
    try:
        registration = Registration.objects.get(id=registration_id)
    except Registration.DoesNotExist:
        logger.error(f"[Task] send_correction_completed_notification: Registration {registration_id} not found.")
        return

    try:
        # 1. Email notification (Independent)
        try:
            logger.info(f"[Task] send_correction_completed_notification: Sending email for {registration_id}")
            send_correction_completed_email(registration)
        except Exception as e:
            logger.error(f"[Task] send_correction_completed_notification: Email failed: {str(e)}")

        # 2. WhatsApp notification (New template correction_done_v1)
        logger.info(f"[Task] send_correction_completed_notification: Sending WhatsApp for {registration_id}")
        result = send_correction_done_v1(
            phone=registration.phone_number,
            full_name=registration.full_name
        )
        
        if result.get('success'):
            logger.info(f"[Task] send_correction_completed_notification: ✓ WhatsApp sent for {registration_id}")
        else:
            # We don't retry if it's a template missing error (likely in production before Meta approval)
            error_data = result.get('response', {}).get('error', {})
            error_msg = error_data.get('message', 'Unknown WhatsApp error')
            logger.error(f"[Task] send_correction_completed_notification: ❌ WhatsApp failed: {error_msg}")
    except Exception as exc:
        logger.error(f"[Task] send_correction_completed_notification: Unexpected error: {str(exc)}")

# Voice reminder system isolated from core registration logic.
# Failure here must never affect registration or allotment.

@shared_task(name='registrations.schedule_voice_reminder')
def schedule_voice_reminder_task(duty_assignment_id):
    """
    Calculates reporting time and schedules a DutyReminderCall 2 hours before.
    Isolated from core flow. No block on failure.
    """
    from .models import DutyAssignment, DutyReminderCall
    from .utils.reporting import get_reporting_time
    from datetime import datetime, timedelta
    import pytz

    try:
        assignment = DutyAssignment.objects.select_related('assigned_user').get(id=duty_assignment_id)
        
        # 1. Safety check: Check if PENDING reminder already exists for this duty
        existing = DutyReminderCall.objects.filter(
            duty_assignment=assignment,
            call_status='PENDING'
        ).first()
        
        if existing:
            logger.info(f"[VoiceTask] Pending reminder already exists for duty {duty_assignment_id}. Skipping.")
            return

        reporting_time_str = get_reporting_time(assignment)
        if not reporting_time_str:
            logger.warning(f"[VoiceTask] No reporting time rule for assignment {duty_assignment_id}")
            return

        # Timezone Logic Implementation
        ist = pytz.timezone('Asia/Kolkata')
        time_obj = datetime.strptime(reporting_time_str, "%I:%M %p").time()
        
        naive_dt = datetime.combine(assignment.duty_date, time_obj)
        aware_dt_ist = ist.localize(naive_dt)
        
        # Subtract 2 hours
        scheduled_time_ist = aware_dt_ist - timedelta(hours=2)
        scheduled_time_utc = scheduled_time_ist.astimezone(pytz.UTC)
        
        # Debug Logs (Requirement 1)
        logger.info(f"[VoiceTask] Timezone Validation for duty {duty_assignment_id}:")
        logger.info(f"  Reporting Time IST: {aware_dt_ist}")
        logger.info(f"  Scheduled Time IST: {scheduled_time_ist}")
        logger.info(f"  Scheduled Time UTC: {scheduled_time_utc}")
        logger.info(f"  Current UTC: {timezone.now()}")

        # Create record (Requirement 2: Duplicate protection)
        reminder, created = DutyReminderCall.objects.get_or_create(
            registration=assignment.assigned_user,
            duty_assignment=assignment,
            scheduled_time=scheduled_time_utc,
            defaults={'call_status': 'PENDING'}
        )
        
        if created:
            logger.info(f"[VoiceTask] Scheduled new call for {assignment.assigned_user.its_number} at {scheduled_time_utc}")
        else:
            logger.info(f"[VoiceTask] Voice reminder already exists for {assignment.assigned_user.its_number} at {scheduled_time_utc}")

    except DutyAssignment.DoesNotExist:
        logger.error(f"[VoiceTask] DutyAssignment {duty_assignment_id} not found")
    except Exception as e:
        logger.error(f"[VoiceTask] [Isolated] Failed to schedule voice reminder: {str(e)}")


@shared_task(name='registrations.process_due_reminder_calls')
def process_due_reminder_calls_task():
    """
    Periodic task to trigger due voice calls.
    Uses select_for_update() and transaction.atomic() for race condition safety.
    """
    from .models import DutyReminderCall
    from .utils.exotel import make_exotel_call
    from .utils.reporting import get_reporting_time
    from django.db import transaction
    
    now = timezone.now()
    
    try:
        with transaction.atomic():
            # select_for_update() prevents other workers from picking the same row
            due_calls = DutyReminderCall.objects.select_for_update(skip_locked=True).filter(
                call_status='PENDING',
                scheduled_time__lte=now
            ).select_related('registration', 'duty_assignment')

            if not due_calls.exists():
                return
            
            logger.info(f"[VoiceTask] Processing {due_calls.count()} due voice reminders")
            
            for call in due_calls:
                try:
                    reporting_time = get_reporting_time(call.duty_assignment)
                    
                    # Log attempt
                    logger.info(f"[VoiceTask] [Worker] Calling Exotel for CallID: {call.id}")
                    
                    result = make_exotel_call(call.registration, call.duty_assignment, reporting_time)
                    
                    if result.get('success'):
                        call.call_status = 'SENT'
                        call.exotel_call_sid = result.get('call_sid')
                        logger.info(f"[VoiceTask] Call SUCCESS: {call.exotel_call_sid}")
                    else:
                        call.call_status = 'FAILED'
                        error_msg = result.get('error')
                        logger.error(f"[VoiceTask] Call FAILED for {call.id}: {error_msg}")
                    
                    call.save()
                    
                except Exception as e:
                    logger.error(f"[VoiceTask] Error in loop for call {call.id}: {str(e)}")
                    call.call_status = 'FAILED'
                    call.save()
                    
    except Exception as exc:
        logger.error(f"[VoiceTask] [Fatal] Periodic task failed: {str(exc)}")
