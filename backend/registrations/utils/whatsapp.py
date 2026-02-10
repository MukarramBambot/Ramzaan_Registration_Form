"""
WhatsApp integration via official Meta Cloud API.

Handles:
- Registration confirmation
- Duty allotment notification
- 24-hour event reminders
"""

import json
import logging
import requests
from django.conf import settings

logger = logging.getLogger("registrations")

# -------------------------------------------------------------------
# Meta Configuration
# -------------------------------------------------------------------

META_WA_PHONE_NUMBER_ID = getattr(settings, "META_WA_PHONE_NUMBER_ID", "")
META_WA_ACCESS_TOKEN = getattr(settings, "META_WA_ACCESS_TOKEN", "")
META_WA_API_VERSION = getattr(settings, "META_WA_API_VERSION", "v18.0")

# Template Names (Meta uses names, not SIDs)
TEMPLATE_FORM_SUBMITTED = "form_submitted_notification"
TEMPLATE_ALLOTMENT = "allotment_confirmed"
TEMPLATE_REMINDER = "event_reminder_24hrs"

def normalize_phone_number(number):
    """
    Normalize phone number to digits only (Meta API requirement).
    - Strips +, space, dashes
    - Ensures country code is present (assumes 91 if 10 digits)
    """
    if not number:
        return None

    digits = "".join(filter(str.isdigit, str(number)))

    if len(digits) == 10:
        return f"91{digits}"
    return digits

def send_meta_whatsapp_template(to_number, template_name, components):
    """
    Core WhatsApp sender using Meta Cloud API.
    
    Args:
        to_number (str): recipient phone number
        template_name (str): The name of the approved Meta template
        components (list): List of component dicts (body parameters)
    """
    if not META_WA_ACCESS_TOKEN or not META_WA_PHONE_NUMBER_ID:
        logger.error("[WhatsApp] Meta API credentials missing in settings")
        return False

    phone_number = normalize_phone_number(to_number)
    if not phone_number:
        logger.error(f"[WhatsApp] Invalid phone number: {to_number}")
        return False

    url = f"https://graph.facebook.com/{META_WA_API_VERSION}/{META_WA_PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {META_WA_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": "en"
            },
            "components": components
        }
    }

    try:
        logger.info(f"[WhatsApp] Sending Meta template '{template_name}' to {phone_number}")
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response_data = response.json()

        if response.status_code == 200:
            logger.info(f"[WhatsApp] ✓ SENT (Meta ID: {response_data.get('messages', [{}])[0].get('id')})")
            return True
        else:
            logger.error(f"[WhatsApp] Meta API Error: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        logger.exception(f"[WhatsApp] Unexpected error during Meta API call: {str(e)}")
        return False

# -------------------------------------------------------------------
# Public Notification APIs
# -------------------------------------------------------------------

def send_registration_notification(registration):
    """
    Template: form_submitted_notification
    V1: Full Name
    """
    components = [
        {
            "type": "body",
            "parameters": [
                {"type": "text", "text": registration.full_name}
            ]
        }
    ]
    return send_meta_whatsapp_template(registration.phone_number, TEMPLATE_FORM_SUBMITTED, components)

def send_duty_allotment_notification(duty_assignment):
    """
    Template: allotment_confirmed
    V1: Full Name
    V2: Date
    V3: Time
    """
    user = duty_assignment.assigned_user
    date_str = duty_assignment.duty_date.strftime("%d %B %Y")
    
    if hasattr(duty_assignment, "slot") and duty_assignment.slot:
        time_str = duty_assignment.slot.time_label
    else:
        time_str = duty_assignment.get_namaaz_type_display()

    components = [
        {
            "type": "body",
            "parameters": [
                {"type": "text", "text": user.full_name},
                {"type": "text", "text": date_str},
                {"type": "text", "text": time_str}
            ]
        }
    ]
    return send_meta_whatsapp_template(user.phone_number, TEMPLATE_ALLOTMENT, components)

def send_event_reminder_24hrs(registration, date, time_label):
    """
    Template: event_reminder_24hrs
    V1: Full Name
    V2: Date
    V3: Time
    """
    components = [
        {
            "type": "body",
            "parameters": [
                {"type": "text", "text": registration.full_name},
                {"type": "text", "text": str(date)},
                {"type": "text", "text": str(time_label)}
            ]
        }
    ]
    return send_meta_whatsapp_template(registration.phone_number, TEMPLATE_REMINDER, components)
