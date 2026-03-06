"""
Celery tasks for Vajebaat appointment notifications and Google Sheets sync.
Offloading heavy synchronous I/O from the request-response cycle.
"""

from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task(name='vajebaat.sync_to_sheets')
def sync_vajebaat_to_sheets_task():
    """
    Background task to perform full sync of Vajebaat appointments to Google Sheets.
    """
    logger.info("[Task] Starting Vajebaat Google Sheets sync...")
    try:
        from .google_sheets import sync_vajebaat_members
        success, detail = sync_vajebaat_members()
        if success:
            logger.info(f"[Task] Vajebaat Sheet sync SUCCESS: {detail} records.")
        else:
            logger.error(f"[Task] Vajebaat Sheet sync FAILED: {detail}")
        return success
    except Exception as e:
        logger.error(f"[Task] Vajebaat Sheet sync CRITICAL ERROR: {e}")
        return False

@shared_task(name='vajebaat.send_appointment_confirmation')
def send_appointment_confirmation_task(appointment_id):
    """
    Background task to send WhatsApp + Email for a new appointment.
    """
    from .models import VajebaatAppointment
    from .notifications import send_vajebaat_notification

    logger.info(f"[Task] Sending confirmation for Appointment {appointment_id}...")
    try:
        appointment = VajebaatAppointment.objects.get(id=appointment_id)
        send_vajebaat_notification(appointment, 'CREATED')
        return True
    except VajebaatAppointment.DoesNotExist:
        logger.error(f"[Task] Notification failed: Appointment {appointment_id} not found.")
        return False
    except Exception as e:
        logger.error(f"[Task] Notification failed for Appointment {appointment_id}: {e}")
        return False

@shared_task(name='vajebaat.send_slot_confirmed_notification')
def send_slot_confirmed_notification_task(appointment_id, slot_id):
    """
    Background task to send WhatsApp + Email when a slot is assigned.
    """
    from .models import VajebaatAppointment, VajebaatSlot
    from .notifications import send_vajebaat_notification

    logger.info(f"[Task] Sending Slot Confirmed notification for Appointment {appointment_id}...")
    try:
        appointment = VajebaatAppointment.objects.get(id=appointment_id)
        slot = VajebaatSlot.objects.get(id=slot_id)
        send_vajebaat_notification(appointment, 'CONFIRMED', slot=slot)
        return True
    except Exception as e:
        logger.error(f"[Task] Slot Confirmed notifications failed: {e}")
        return False

@shared_task(name='vajebaat.send_slot_rescheduled_notification')
def send_slot_rescheduled_notification_task(appointment_id, slot_id):
    """
    Background task to send WhatsApp + Email when a slot is rescheduled.
    """
    from .models import VajebaatAppointment, VajebaatSlot
    from .notifications import send_vajebaat_notification

    logger.info(f"[Task] Sending Slot Rescheduled notification for Appointment {appointment_id}...")
    try:
        appointment = VajebaatAppointment.objects.get(id=appointment_id)
        slot = VajebaatSlot.objects.get(id=slot_id)
        send_vajebaat_notification(appointment, 'RESCHEDULED', slot=slot)
        return True
    except Exception as e:
        logger.error(f"[Task] Slot Rescheduled notification failed: {e}")
        return False

@shared_task(name='vajebaat.send_appointment_cancelled_notification')
def send_appointment_cancelled_notification_task(appointment_id, slot_id=None):
    """
    Background task to send WhatsApp + Email when an appointment is cancelled.
    """
    from .models import VajebaatAppointment, VajebaatSlot
    from .notifications import send_vajebaat_notification

    logger.info(f"[Task] Sending Appointment Cancelled notification for Appointment {appointment_id}...")
    try:
        appointment = VajebaatAppointment.objects.get(id=appointment_id)
        slot = None
        if slot_id:
            try:
                slot = VajebaatSlot.objects.get(id=slot_id)
            except VajebaatSlot.DoesNotExist:
                pass
        
        send_vajebaat_notification(appointment, 'CANCELLED', slot=slot)
        return True
    except Exception as e:
        logger.error(f"[Task] Appointment Cancelled notification failed: {e}")
        return False
