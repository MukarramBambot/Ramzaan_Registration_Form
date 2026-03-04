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
        logger.warning("WhatsApp: no phone number provided, skipping.")
        return False

    phone = _clean_phone(phone)

    phone_id = getattr(settings, 'META_WA_PHONE_NUMBER_ID', None)
    access_token = getattr(settings, 'META_WA_ACCESS_TOKEN', None)
    api_version = getattr(settings, 'META_WA_API_VERSION', None) or 'v24.0'

    if not phone_id or not access_token:
        logger.warning("WhatsApp API credentials not configured, skipping template '%s'.", template_name)
        return False

    url = f"https://graph.facebook.com/{api_version}/{phone_id}/messages"

    # Build template parameters
    components = []
    if variables:
        parameters = [
            {"type": "text", "text": str(v)} for v in variables
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

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        if resp.status_code in (200, 201):
            logger.info(
                "WhatsApp template '%s' sent to %s",
                template_name, phone,
            )
            return True
        else:
            logger.error(
                "WhatsApp template '%s' failed (%d): %s",
                template_name, resp.status_code, resp.text,
            )
            return False
    except requests.Timeout:
        logger.error("WhatsApp template '%s' timed out for %s", template_name, phone)
        return False
    except Exception as e:
        logger.error("WhatsApp template '%s' error for %s: %s", template_name, phone, e)
        return False


# ============================================================
# Convenience wrappers for each lifecycle event
# ============================================================

def notify_request_received(appointment):
    """Send vajebaat_req_received_v1 when user submits an appointment."""
    send_whatsapp_template(
        phone=appointment.mobile,
        template_name='vajebaat_req_received_v1',
        variables=[
            appointment.name,
            str(appointment.preferred_date) if appointment.preferred_date else 'TBD',
            'To be assigned',
        ],
    )


def notify_slot_confirmed(appointment, slot):
    """Send vajebaat_slot_confirmed_v1 when admin assigns a slot."""
    date_str = slot.date.date.strftime('%d %B %Y')
    slot_time = f"{slot.start_time.strftime('%H:%M')} – {slot.end_time.strftime('%H:%M')}"
    send_whatsapp_template(
        phone=appointment.mobile,
        template_name='vajebaat_slot_confirmed_v1',
        variables=[appointment.name, date_str, slot_time],
    )


def notify_slot_rescheduled(appointment, new_slot):
    """Send vajebaat_slot_rescheduled_v1 when admin reschedules."""
    date_str = new_slot.date.date.strftime('%d %B %Y')
    slot_time = f"{new_slot.start_time.strftime('%H:%M')} – {new_slot.end_time.strftime('%H:%M')}"
    send_whatsapp_template(
        phone=appointment.mobile,
        template_name='vajebaat_slot_rescheduled_v1',
        variables=[appointment.name, date_str, slot_time],
    )


def notify_appointment_cancelled(appointment, slot=None):
    """Send vajebaat_appointment_cancel_v1 when admin cancels."""
    date_str = str(appointment.preferred_date) if appointment.preferred_date else 'N/A'
    slot_time = 'N/A'
    if slot:
        date_str = slot.date.date.strftime('%d %B %Y')
        slot_time = f"{slot.start_time.strftime('%H:%M')} – {slot.end_time.strftime('%H:%M')}"

from django.core.mail import send_mail

def send_confirmation_email(to_email, name, date_str, slot_time):
    """
    Send a Vajebaat appointment confirmation email.

    Args:
        to_email: Recipient email address
        name: Recipient name
        date_str: Formatted appointment date string
        slot_time: Formatted time slot string (e.g., "10:00 – 10:15")
    """
    if not to_email:
        logger.warning("No email address provided, skipping email.")
        return False

    subject = "Vajebaat Appointment Confirmed – Sherullah 1447H"
    body = (
        f"Assalamu Alaikum {name},\n\n"
        f"Your Vajebaat appointment has been confirmed.\n\n"
        f"📅 Date: {date_str}\n"
        f"⏰ Time Slot: {slot_time}\n\n"
        f"Please arrive on time at Saifee Masjid, Chennai.\n\n"
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
        logger.info(f"Confirmation email sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False
