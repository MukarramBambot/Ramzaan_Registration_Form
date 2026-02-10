"""
Twilio WhatsApp integration for PRODUCTION (Content Templates).

Handles:
- Registration confirmation
- Duty allotment notification
- 24-hour event reminders
"""

import json
import logging
import os

from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger("registrations")

# -------------------------------------------------------------------
# Twilio Client (single instance)
# -------------------------------------------------------------------

TWILIO_ACCOUNT_SID = getattr(settings, "TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = getattr(settings, "TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_FROM = getattr(settings, "TWILIO_WHATSAPP_FROM", "")

if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
else:
    twilio_client = None
    logger.error("[WhatsApp] Twilio credentials missing in settings")


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def normalize_phone_number(number):
    """
    Normalize phone number to E.164 format for WhatsApp.

    - Strips non-digits
    - Defaults to India (+91) for 10-digit numbers
    """
    if not number:
        return None

    digits = "".join(filter(str.isdigit, str(number)))

    if len(digits) == 10:
        return f"+91{digits}"
    if len(digits) == 12 and digits.startswith("91"):
        return f"+{digits}"
    if len(digits) > 10:
        return f"+{digits}"

    return None


def send_whatsapp_template(to_number, content_sid, content_variables):
    """
    Core WhatsApp sender using Twilio Content Templates.

    Args:
        to_number (str): Raw phone number
        content_sid (str): HX... template SID
        content_variables (dict): Template variables
    """
    if not twilio_client:
        logger.error("[WhatsApp] Twilio client not initialized")
        return False

    e164_number = normalize_phone_number(to_number)
    if not e164_number:
        logger.error(f"[WhatsApp] Invalid phone number: {to_number}")
        return False

    try:
        logger.info(
            f"[WhatsApp] Sending template {content_sid} → {e164_number} "
            f"vars={content_variables}"
        )

        message = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=f"whatsapp:{e164_number}",
            content_sid=content_sid,
            content_variables=json.dumps(content_variables),
        )

        logger.info(f"[WhatsApp] ✓ SENT SID={message.sid}")
        return True

    except TwilioRestException as e:
        logger.error(
            f"[WhatsApp] Twilio error: {e.msg} (code={e.code})"
        )

        # Sandbox-specific failure
        if e.code == 63016:
            return "SANDBOX"

        return False

    except Exception as e:
        logger.exception(f"[WhatsApp] Unexpected error: {str(e)}")
        return False


# -------------------------------------------------------------------
# Public Notification APIs
# -------------------------------------------------------------------

def send_registration_notification(registration):
    """
    Template: form_submitted_notification
    {{1}} -> Full Name
    """
    content_sid = getattr(settings, "TWILIO_TEMPLATE_FORM_SUBMITTED", "")
    if not content_sid:
        logger.error("[WhatsApp] Missing TWILIO_TEMPLATE_FORM_SUBMITTED")
        return False

    return send_whatsapp_template(
        to_number=registration.phone_number,
        content_sid=content_sid,
        content_variables={
            "1": registration.full_name
        },
    )


def send_duty_allotment_notification(duty_assignment):
    """
    Template: allotment_confirmed
    {{1}} -> Full Name
    {{2}} -> Date (12 March 2026)
    {{3}} -> Time (6:30 AM)
    """
    content_sid = getattr(settings, "TWILIO_TEMPLATE_ALLOTMENT", "")
    if not content_sid:
        logger.error("[WhatsApp] Missing TWILIO_TEMPLATE_ALLOTMENT")
        return False

    user = duty_assignment.assigned_user

    date_str = duty_assignment.duty_date.strftime("%d %B %Y")

    if hasattr(duty_assignment, "slot") and duty_assignment.slot:
        time_str = duty_assignment.slot.time_label
    else:
        time_str = duty_assignment.get_namaaz_type_display()

    return send_whatsapp_template(
        to_number=user.phone_number,
        content_sid=content_sid,
        content_variables={
            "1": user.full_name,
            "2": date_str,
            "3": time_str,
        },
    )


def send_event_reminder_24hrs(registration, date, time_label):
    """
    Template: event_reminder_24hrs
    {{1}} -> Full Name
    {{2}} -> Date
    {{3}} -> Time
    """
    content_sid = getattr(settings, "TWILIO_TEMPLATE_REMINDER", "")
    if not content_sid:
        logger.error("[WhatsApp] Missing TWILIO_TEMPLATE_REMINDER")
        return False

    return send_whatsapp_template(
        to_number=registration.phone_number,
        content_sid=content_sid,
        content_variables={
            "1": registration.full_name,
            "2": str(date),
            "3": str(time_label),
        },
    )
