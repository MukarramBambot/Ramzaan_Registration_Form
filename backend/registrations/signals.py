from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
import logging

from .models import Registration, DutyAssignment
from .utils import safe_task_delay
from .tasks import (
    send_registration_confirmation_task, 
    send_duty_allotment_notification_task,
    sync_to_sheets_task
)
from .utils.email_notifications import send_registration_email, send_allotment_email

logger = logging.getLogger('registrations')


@receiver(post_save, sender=Registration)
def registration_post_save(sender, instance, created, **kwargs):
    """
    Trigger WhatsApp + Email notification for new registrations.
    
    Only fires on creation (created=True), not on updates.
    Uses transaction.on_commit to ensure DB is ready before task runs.
    Delegates to Celery task which runs async and never blocks API response.
    """
    if not created:
        return  # Only handle new registrations
    
    logger.info(f"[Signal] registration_post_save: New registration {instance.id} ({instance.full_name}). Will schedule tasks after commit.")
    
    def schedule_tasks():
        """Enqueue tasks after transaction commits.
        """
        # 1. Notifications are handled in the background task

        # 2. WhatsApp + Email Notification (Async via Celery)
        try:
            logger.info(f"[OnCommit] Enqueueing notifications for registration {instance.id}")
            safe_task_delay(send_registration_confirmation_task, instance.id, non_blocking=True)
        except Exception as e:
            logger.error(f"[OnCommit] Failed to schedule notification task for registration {instance.id}: {str(e)}")

        # 3. Google Sheets Sync (Async via Celery)
        try:
            logger.info(f"[OnCommit] Enqueueing sync_to_sheets_task for registration {instance.id}")
            safe_task_delay(sync_to_sheets_task, instance.id, non_blocking=True)
        except Exception as e:
            logger.error(f"[OnCommit] Failed to schedule sheet sync task for registration {instance.id}: {str(e)}")
    
    try:
        # Schedule the function to run AFTER this transaction commits.
        # This ensures the registration record is saved to DB before the task tries to fetch it.
        transaction.on_commit(schedule_tasks)
        logger.info(f"[Signal] on_commit callback registered for registration {instance.id}")
    except Exception as e:
        logger.error(f"[Signal] Failed to register on_commit callback for registration {instance.id}: {str(e)}")


@receiver(post_save, sender=DutyAssignment)
def duty_assignment_post_save(sender, instance, created, **kwargs):
    """
    Trigger WhatsApp notification for new duty assignments.
    
    Only fires on creation (created=True), not on updates.
    Prevents duplicate messages on subsequent signal misfires.
    Uses transaction.on_commit and Celery for async execution.
    """
    if not created:
        return  # Only handle new duty assignments
    
    logger.info(f"[Signal] duty_assignment_post_save: New duty {instance.id} assigned to {instance.assigned_user.full_name}. Will schedule task after commit.")
    
    def schedule_tasks():
        """Enqueue tasks after DB commit.
        """
        # 1. Notifications are handled in the background task

        # 2. WhatsApp Notification (Async via Celery)
        try:
            logger.info(f"[OnCommit] Enqueueing send_duty_allotment_notification_task for duty {instance.id}")
            result = safe_task_delay(send_duty_allotment_notification_task, instance.id, non_blocking=True)
            logger.info(f"[OnCommit] Task scheduled for duty {instance.id}: {result}")
        except Exception as e:
            logger.error(f"[OnCommit] Failed to schedule task for duty {instance.id}: {str(e)}")
    
    try:
        # Schedule the function to run AFTER this transaction commits.
        transaction.on_commit(schedule_tasks)
        logger.info(f"[Signal] on_commit callback registered for duty {instance.id}")
    except Exception as e:
        logger.error(f"[Signal] Failed to register on_commit callback for duty {instance.id}: {str(e)}")
