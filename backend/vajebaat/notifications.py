"""
WhatsApp notification service for Vajebaat appointment lifecycle.
Uses Meta Cloud API with approved message templates.

Templates:
- vajebaat_req_received_v1       → User submits appointment
- vajebaat_slot_confirmed_v1     → Admin assigns slot
- vajebaat_slot_rescheduled_v1   → Admin reschedules slot
- vajebaat_appointment_cancel_v1 → Admin cancels appointment

All templates use variables: {{1}} Name, {{2}} Date, {{3}} Slot Time
"""

import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def _clean_phone(phone_number):
    """Normalize phone number for WhatsApp API (digits only, with country code)."""
    phone = phone_number.strip().replace('+', '').replace(' ', '').replace('-', '')
    # Indian number without country code → prepend 91
    if len(phone) == 10 and phone[0] in ('6', '7', '8', '9'):
        phone = '91' + phone
    return phone


def _mask_phone(phone: str) -> str:
    """Mask phone number for logging privacy."""
    if not phone or len(phone) < 4:
        return "****"
    return "*" * (len(phone) - 4) + phone[-4:]


def _sanitize_param(v):
    """
    Sanitize parameters for Meta WhatsApp API.
    Restriction: No newlines, no tabs, no >4 consecutive spaces.
    """
    if v is None:
        return ""
    # Replace newlines/tabs with space and collapse multiple spaces
    return " ".join(str(v).replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').split())


def send_whatsapp_template(phone, template_name, variables):
    """
    Send a WhatsApp template message via Meta Cloud API.

    Args:
        phone: Recipient phone number (raw — will be cleaned)
        template_name: Approved template name (e.g. 'vajebaat_slot_confirmed_v1')
        variables: List of template variable strings [name, date, slot_time]

    Returns:
        True if sent successfully, False otherwise.
    """
    if not phone:
        logger.warning("Skipping notification — member has no phone number.")
        return False

    phone = _clean_phone(phone)

    phone_id = getattr(settings, 'WHATSAPP_PHONE_NUMBER_ID', None)
    access_token = getattr(settings, 'WHATSAPP_ACCESS_TOKEN', None)
    api_version = getattr(settings, 'WHATSAPP_API_VERSION', 'v24.0')

    if not phone_id or not access_token:
        logger.warning("WhatsApp API credentials (WHATSAPP_*) not configured, skipping template '%s'.", template_name)
        return False

    # Defensive validation: All current Vajebaat templates require exactly 3 parameters
    # {{1}} = Name, {{2}} = Date, {{3}} = Slot Time
    if variables and len(variables) != 3:
        logger.error(f"[WhatsApp] Parameter mismatch for '{template_name}': Expected 3, got {len(variables)}")
        return False

    url = f"https://graph.facebook.com/{api_version}/{phone_id}/messages"

    # Build template parameters with sanitization
    components = []
    if variables:
        sanitized_variables = [_sanitize_param(v) for v in variables]
        parameters = [
            {"type": "text", "text": v} for v in sanitized_variables
        ]
        components.append({
            "type": "body",
            "parameters": parameters,
        })

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": "en"},
            "components": components,
        },
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    masked_phone = _mask_phone(phone)
    logger.info(f"[WhatsApp] Sending template '{template_name}' to {masked_phone} with params: {variables}")

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        import json
        try:
            response_data = resp.json()
        except ValueError:
            response_data = {"raw_text": resp.text}

        if resp.status_code in (200, 201):
            msg_id = response_data.get("messages", [{}])[0].get("id")
            logger.info(
                "WhatsApp template '%s' sent to %s | MsgID: %s",
                template_name, phone, msg_id
            )
            return True
        else:
            logger.error(
                "WhatsApp template '%s' failed (%d): %s",
                template_name, resp.status_code, json.dumps(response_data),
            )
            return False
    except requests.Timeout:
        logger.error("WhatsApp template '%s' timed out for %s", template_name, phone)
        return False
    except Exception as e:
        logger.error("WhatsApp template '%s' error for %s: %s", template_name, phone, e)
        return False


# ============================================================
# UNIFIED NOTIFICATION SERVICE
# ============================================================

def send_vajebaat_notification(appointment, event_type, slot=None):
    """
    Unified function to send BOTH WhatsApp and Email notifications.
    
    event_type: 'CREATED', 'CONFIRMED', 'RESCHEDULED', 'CANCELLED'
    """
    logger.info(f"[Notify] Processing {event_type} for Appointment {appointment.id} (ITS: {appointment.its_number})")
    
    # 1. Prepare Data
    name = appointment.name
    phone = appointment.mobile
    email = appointment.email
    
    date_str = "TBD"
    slot_time = "To be assigned"
    
    if event_type == 'CREATED':
        whatsapp_template = 'vajebaat_req_received_v1'
        email_subject = "Vajebaat Appointment Request Received – Sherullah 1447H"
        date_str = str(appointment.preferred_date) if appointment.preferred_date else 'TBD'
    
    elif event_type == 'CONFIRMED':
        whatsapp_template = 'vajebaat_slot_confirmed_v1'
        email_subject = "Vajebaat Appointment Confirmed – Sherullah 1447H"
        if slot:
            date_str = slot.date.date.strftime('%d %B %Y')
            slot_time = f"{slot.start_time.strftime('%H:%M')} – {slot.end_time.strftime('%H:%M')}"

    elif event_type == 'RESCHEDULED':
        whatsapp_template = 'vajebaat_slot_rescheduled_v1'
        email_subject = "Vajebaat Appointment Rescheduled – Sherullah 1447H"
        if slot:
            date_str = slot.date.date.strftime('%d %B %Y')
            slot_time = f"{slot.start_time.strftime('%H:%M')} – {slot.end_time.strftime('%H:%M')}"

    elif event_type == 'CANCELLED':
        whatsapp_template = 'vajebaat_appointment_cancel_v1'
        email_subject = "Vajebaat Appointment Cancelled – Sherullah 1447H"
        if slot:
            date_str = slot.date.date.strftime('%d %B %Y')
            slot_time = f"{slot.start_time.strftime('%H:%M')} – {slot.end_time.strftime('%H:%M')}"
        else:
            date_str = str(appointment.preferred_date) if appointment.preferred_date else 'N/A'
            slot_time = 'N/A'
    else:
        logger.error(f"[Notify] Unknown event type: {event_type}")
        return False

    # 2. Send WhatsApp
    ws_success = send_whatsapp_template(
        phone=phone,
        template_name=whatsapp_template,
        variables=[name, date_str, slot_time]
    )
    if ws_success:
        logger.info(f"[Notify] WhatsApp notification sent for {event_type}")
    else:
        logger.warning(f"[Notify] WhatsApp notification failed/skipped for {event_type}")

    # 3. Send Email
    if email:
        em_success = send_vajebaat_email(
            to_email=email,
            subject=email_subject,
            name=name,
            date_str=date_str,
            slot_time=slot_time,
            event_type=event_type
        )
        if em_success:
            logger.info(f"[Notify] Email notification sent for {event_type}")
        else:
            logger.warning(f"[Notify] Email notification failed for {event_type}")
    else:
        logger.warning(f"[Notify] Email skipped — no email address for Appointment {appointment.id}")
        em_success = False

    return ws_success or em_success


from django.core.mail import send_mail

def send_vajebaat_email(to_email, subject, name, date_str, slot_time, event_type):
    """Generic email sender for Vajebaat events."""
    if not to_email:
        return False

    if event_type == 'CREATED':
        status_msg = "Your request for a Vajebaat appointment has been received. We will assign a slot shortly."
    elif event_type == 'CONFIRMED':
        status_msg = "Your Vajebaat appointment has been confirmed for the following slot."
    elif event_type == 'RESCHEDULED':
        status_msg = "Your Vajebaat appointment has been rescheduled to the following new slot."
    elif event_type == 'CANCELLED':
        status_msg = "Your Vajebaat appointment has been cancelled."
    else:
        status_msg = "Notification regarding your Vajebaat appointment."

    body = (
        f"Assalamu Alaikum {name},\n\n"
        f"{status_msg}\n\n"
        f"📅 Date: {date_str}\n"
        f"⏰ Time Slot: {slot_time}\n\n"
        f"Location: Saifee Masjid, Chennai.\n\n"
        f"JazakAllah Khair,\n"
        f"Madras Jamaat Portal"
    )

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False


# Legacy wrappers (refactored to use unified service if possible, or kept for compatibility if tasks call them directly)
def notify_request_received(appointment):
    return send_vajebaat_notification(appointment, 'CREATED')

def notify_slot_confirmed(appointment, slot):
    return send_vajebaat_notification(appointment, 'CONFIRMED', slot=slot)

def notify_slot_rescheduled(appointment, new_slot):
    return send_vajebaat_notification(appointment, 'RESCHEDULED', slot=new_slot)

def notify_appointment_cancelled(appointment, slot=None):
    return send_vajebaat_notification(appointment, 'CANCELLED', slot=slot)
