from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
import logging
import os

from .models import Registration, DutyAssignment, AuditionFile
from .utils import safe_task_delay
from .tasks import (
    send_registration_confirmation_task, 
    send_duty_allotment_notification_task,
    sync_to_sheets_task,
    schedule_voice_reminder_task
)
from .utils.email_notifications import send_registration_email, send_allotment_email

logger = logging.getLogger('registrations')


# NOTE: Registration tasks (confirmation, sheet sync) are now triggered directly 
# in the RegistrationViewSet.create method using transaction.on_commit 
# for better reliability and to ensure only IDs are passed.
# See: registrations/views.py


@receiver(post_save, sender=DutyAssignment)
def duty_assignment_post_save(sender, instance, created, **kwargs):
    """
    Trigger WhatsApp notification for new duty assignments.
    """
    if not created:
        return
    
    logger.info(f"[Signal] duty_assignment_post_save: New duty {instance.id} assigned to {instance.assigned_user.full_name}. Will schedule task after commit.")
    
    # Update registration status to ALLOTTED
    try:
        registration = instance.assigned_user
        if registration.status != 'ALLOTTED':
            registration.status = 'ALLOTTED'
            registration.save(update_fields=['status'])
            logger.info(f"[Signal] Updated registration {registration.id} status to ALLOTTED")
    except Exception as e:
        logger.error(f"[Signal] Failed to update registration status for duty {instance.id}: {str(e)}")
    
    def schedule_tasks():
        try:
            logger.info(f"[OnCommit] Enqueueing send_duty_allotment_notification_task for duty {instance.id}")
            result = safe_task_delay(send_duty_allotment_notification_task, instance.id, non_blocking=True)
            logger.info(f"[OnCommit] Task scheduled for duty {instance.id}: {result}")
        except Exception as e:
            logger.error(f"[OnCommit] Failed to schedule task for duty {instance.id}: {str(e)}")
    
    # Schedule voice reminder
    try:
        transaction.on_commit(lambda: safe_task_delay(schedule_voice_reminder_task, instance.id, non_blocking=True))
        logger.info(f"[Signal] Voice reminder scheduling task enqueued for duty {instance.id}")
    except Exception as e:
        logger.error(f"[Signal] Failed to enqueue voice reminder task for duty {instance.id}: {str(e)}")

    try:
        transaction.on_commit(schedule_tasks)
        logger.info(f"[Signal] on_commit callback registered for duty {instance.id}")
    except Exception as e:
        logger.error(f"[Signal] Failed to register on_commit callback for duty {instance.id}: {str(e)}")


@receiver(post_delete, sender=AuditionFile)
def audition_file_post_delete(sender, instance, **kwargs):
    """
    Delete physical file from disk when AuditionFile record is deleted.
    """
    if instance.audition_file_path:
        try:
            if os.path.isfile(instance.audition_file_path.path):
                os.remove(instance.audition_file_path.path)
                logger.info(f"[Signal] Deleted file from disk: {instance.audition_file_path.path}")
        except Exception as e:
            logger.error(f"[Signal] Failed to delete file or access path: {str(e)}")
