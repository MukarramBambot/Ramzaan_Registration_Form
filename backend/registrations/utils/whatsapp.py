"""
WhatsApp Integration Module (Production Grade)

This module handles sending WhatsApp template messages via the Meta Cloud API.
It allows for:
- sending registration confirmations
- sending duty allotment notifications
- sending duty reminders

Architecture:
- Internal helper `_send_template_message` handles the raw API call with robust logging and error handling.
- Public wrapper functions (`send_duty_allotment`, etc.) strictly define the parameters and templates.

Configuration:
- Requires `WHATSAPP_PHONE_NUMBER_ID` and `WHATSAPP_ACCESS_TOKEN` in Django settings.
- defaults to API version `v24.0` (configurable).

Usage:
    from registrations.utils.whatsapp import send_registration_received
    result = send_registration_received("919876543210", "Ali Bhai")
    if result["success"]:
        print("Message sent!")

"""

import requests
import logging
import json
from typing import Dict, Any, Optional, List
from django.conf import settings
from requests.exceptions import Timeout, ConnectionError, RequestException

# Configure Logger to use the 'registrations' logger defined in settings
logger = logging.getLogger("registrations")

class WhatsAppAPIException(Exception):
    """Custom exception for WhatsApp API failures."""
    pass

# Template Constants
TEMPLATE_DUTY_ALLOTMENT = "duty_allot_v2"
TEMPLATE_DUTY_REMINDER = "duty_remind_v2"
TEMPLATE_REGISTRATION_RECEIVED = "reg_received_v2"
TEMPLATE_CORRECTION_REQ_V1 = "correction_req_v1"
TEMPLATE_CORRECTION_DONE_V1 = "correction_done_v1"

LANGUAGE_CODE = "en"  # Default Language

def _mask_phone_number(phone: str) -> str:
    """
    Masks phone number for logging privacy.
    Example: 919876543210 -> *******3210
    """
    if not phone:
        return "None"
    if len(phone) < 4:
        return "****"
    return "*" * (len(phone) - 4) + phone[-4:]



from .phone import normalize_phone_number

def _send_template_message(phone: str, template_name: str, parameters: List[str]) -> Dict[str, Any]:
    """
    Internal helper to send a WhatsApp template message.
    ...
    """
    # 1. Configuration & Setup
    api_version = getattr(settings, "WHATSAPP_API_VERSION", "v24.0")
    phone_id = getattr(settings, "WHATSAPP_PHONE_NUMBER_ID", None)
    access_token = getattr(settings, "WHATSAPP_ACCESS_TOKEN", None)
    
    if not phone_id or not access_token:
        logger.critical("[WhatsApp] CRITICAL: Missing WHATSAPP_PHONE_NUMBER_ID or WHATSAPP_ACCESS_TOKEN in settings.")
        return {
            "success": False,
            "status_code": None,
            "message_id": None,
            "response": {"error": "Missing Server Configuration"}
        }

    try:
        normalized_to = normalize_phone_number(phone)
    except ValueError as e:
        logger.error(f"[WhatsApp] Invalid phone number: {_mask_phone_number(str(phone))} - {str(e)}")
        return {
            "success": False,
            "status_code": None,
            "message_id": None,
            "response": {"error": f"Invalid Phone Number: {str(e)}"}
        }

    url = f"https://graph.facebook.com/{api_version}/{phone_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 2. Build Payload
    # 1. Sanitize Parameters (Meta Restriction: No newlines, no >4 consecutive spaces)
    def clean_p(v):
        if v is None: return ""
        return " ".join(str(v).replace('\n', ' ').replace('\r', ' ').split())

    component_parameters = [{"type": "text", "text": clean_p(p)} for p in parameters]

    payload = {
        "messaging_product": "whatsapp",
        "to": normalized_to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": LANGUAGE_CODE},
            "components": [
                {
                    "type": "body",
                    "parameters": component_parameters
                }
            ]
        }
    }

    # 3. Log Request (Masked)
    masked_phone = _mask_phone_number(normalized_to)
    logger.info(f"[WhatsApp] Sending '{template_name}' to {masked_phone} with params: {parameters}")
    logger.debug(f"[WhatsApp] Request URL: {url}")
    # Do NOT log the full payload if it contains sensitive info, but here params are usually safe-ish.
    # We will log it for debug purposes but be careful in high security environments.
    logger.debug(f"[WhatsApp] Payload: {json.dumps(payload)}")

    # 4. Execute Request
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        try:
            response_data = response.json()
        except ValueError:
            response_data = {"raw_text": response.text}

        status_code = response.status_code
        
        # 5. Handle Response
        if status_code in [200, 201]:
            # Success
            msg_id = response_data.get("messages", [{}])[0].get("id")
            logger.info(f"[WhatsApp] ✓ Success: {status_code} | MsgID: {msg_id} | To: {masked_phone}")
            return {
                "success": True,
                "status_code": status_code,
                "message_id": msg_id,
                "response": response_data
            }
        else:
            # API Error
            error_info = response_data.get("error", {})
            error_msg = error_info.get("message", "Unknown Error")
            error_code = error_info.get("code")
            
            logger.error(f"[WhatsApp] ❌ API Error: {status_code} | Code: {error_code} | Msg: {error_msg}")
            logger.error(f"[WhatsApp] Full Response: {json.dumps(response_data)}")
            
            # Check for specific handling (optional)
            if error_code == 132001: 
                logger.warning("[WhatsApp] Template does not exist in this language/name combination.")

            raise WhatsAppAPIException(f"Meta API Error {status_code}: {error_msg}")

    except Timeout:
        logger.error(f"[WhatsApp] ⚠️ Timeout (10s) sending to {masked_phone}")
        return {
            "success": False,
            "status_code": 408, # Request Timeout
            "message_id": None,
            "response": {"error": "Connection Timeout"}
        }
        
    except ConnectionError:
        logger.error(f"[WhatsApp] ⚠️ Connection Error sending to {masked_phone}")
        return {
            "success": False,
            "status_code": 503, # Service Unavailable
            "message_id": None,
            "response": {"error": "Connection Failed"}
        }

    except RequestException as e:
        logger.exception(f"[WhatsApp] ⚠️ Unexpected Request Exception: {str(e)}")
        return {
            "success": False,
            "status_code": 500,
            "message_id": None,
            "response": {"error": str(e)}
        }
        
    except WhatsAppAPIException as e:
        # Re-raised from within logic for caller to handle if they want, 
        # or we just return the failure dict.
        # Here we return the failure dict structure as per requirements.
        return {
            "success": False,
            "status_code": status_code,
            "message_id": None,
            "response": response_data
        }

    except Exception as e:
        logger.exception(f"[WhatsApp] ⚠️ Critical Internal Error: {str(e)}")
        return {
            "success": False,
            "status_code": 500,
            "message_id": None,
            "response": {"error": f"Internal Error: {str(e)}"}
        }


# =============================================================================
# PUBLIC WRAPPER FUNCTIONS
# =============================================================================

def send_duty_allotment(phone: str, full_name: str, duty_date: str, duty_time: str, reporting_time: str = None) -> Dict[str, Any]:
    """
    Sends 'duty_allotment_confirmed' template.
    
    Template Params:
    {{1}} = Full Name
    {{2}} = Date
    {{3}} = Time (with Reporting Time appended)
    """
    # Defensive check for None
    full_name = full_name or "Brother/Sister"
    duty_date = str(duty_date)
    duty_time = str(duty_time)
    
    if reporting_time:
        duty_time = f"{duty_time}\nReporting: {reporting_time}"
    
    params = [full_name, duty_date, duty_time]
    
    return _send_template_message(
        phone=phone,
        template_name=TEMPLATE_DUTY_ALLOTMENT,
        parameters=params
    )

def send_duty_reminder_tomorrow(phone: str, full_name: str, duty_date: str, duty_time: str, reporting_time: str = None) -> Dict[str, Any]:
    """
    Sends 'duty_reminder_tomorrow' template.
    
    Template Params:
    {{1}} = Full Name
    {{2}} = Date
    {{3}} = Time (with Reporting Time appended)
    """
    full_name = full_name or "Brother/Sister"
    duty_date = str(duty_date)
    duty_time = str(duty_time)
    
    if reporting_time:
        duty_time = f"{duty_time}\nReporting: {reporting_time}"
    
    params = [full_name, duty_date, duty_time]
    
    return _send_template_message(
        phone=phone,
        template_name=TEMPLATE_DUTY_REMINDER,
        parameters=params
    )

def send_registration_received(phone: str, full_name: str) -> Dict[str, Any]:
    """
    Sends 'registration_received' template.
    
    Template Params:
    {{1}} = Full Name
    """
    full_name = full_name or "Brother/Sister"
    
    params = [full_name]
    
    return _send_template_message(
        phone=phone,
        template_name=TEMPLATE_REGISTRATION_RECEIVED,
        parameters=params
    )


def _send_text_message(phone: str, text: str) -> Dict[str, Any]:
    """
    Send a plain text WhatsApp message (non-template). Used for admin alerts.
    """
    api_version = getattr(settings, "WHATSAPP_API_VERSION", "v24.0")
    phone_id = getattr(settings, "WHATSAPP_PHONE_NUMBER_ID", None)
    access_token = getattr(settings, "WHATSAPP_ACCESS_TOKEN", None)

    if not phone_id or not access_token:
        logger.critical("[WhatsApp] CRITICAL: Missing WHATSAPP_PHONE_NUMBER_ID or WHATSAPP_ACCESS_TOKEN in settings.")
        return {"success": False, "status_code": None, "response": {"error": "Missing Server Configuration"}}

    try:
        normalized_to = normalize_phone_number(phone)
    except ValueError as e:
        logger.error(f"[WhatsApp] Invalid phone number: {_mask_phone_number(str(phone))} - {str(e)}")
        return {"success": False, "status_code": None, "response": {"error": f"Invalid Phone Number: {str(e)}"}}

    url = f"https://graph.facebook.com/{api_version}/{phone_id}/messages"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": normalized_to,
        "type": "text",
        "text": {"body": str(text)}
    }

    masked_phone = _mask_phone_number(normalized_to)
    logger.info(f"[WhatsApp] Sending text message to {masked_phone}")

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        try:
            data = resp.json()
        except ValueError:
            data = {"raw_text": resp.text}

        if resp.status_code in [200, 201]:
            msg_id = data.get("messages", [{}])[0].get("id")
            logger.info(f"[WhatsApp] ✓ Text Success: {resp.status_code} | MsgID: {msg_id} | To: {masked_phone}")
            return {"success": True, "status_code": resp.status_code, "message_id": msg_id, "response": data}
        else:
            logger.error(f"[WhatsApp] ❌ Text API Error: {resp.status_code} | Response: {data}")
            return {"success": False, "status_code": resp.status_code, "response": data}

    except Exception as e:
        logger.exception(f"[WhatsApp] Text send failed: {str(e)}")
        return {"success": False, "status_code": 500, "response": {"error": str(e)}}


def send_admin_text_message(phone: str, text: str) -> Dict[str, Any]:
    """Convenience wrapper to send a plain text WhatsApp to admin or staff."""
    return _send_text_message(phone, text)

def send_correction_notification(correction) -> Dict[str, Any]:
    """
    Sends correction request notification via WhatsApp text message.
    """
    registration = correction.registration
    phone = registration.phone_number
    # Base URL for correction link
    base_url = "https://madrasjamaatportal.org"
    link = f"{base_url}/correction.php?token={correction.token}"
    
    text = (
        f"Assalamu Alaikum {registration.full_name},\n\n"
        f"An administrator has requested a correction for your registration.\n\n"
        f"Field: {correction.field_name.replace('_', ' ').title()}\n"
        f"Message: {correction.admin_message}\n\n"
        f"Please update here: {link}\n\n"
        f"JazakAllah Khair,\n"
        f"Jamaat Administration"
    )
    
    return _send_text_message(phone, text)


def send_correction_req_v1(phone: str, full_name: str, field_name: str, correction_link: str) -> Dict[str, Any]:
    """
    Sends 'correction_req_v1' template.
    Variables: {{1}}=Name, {{2}}=Field, {{3}}=Link
    """
    params = [full_name or "Brother/Sister", field_name, correction_link]
    return _send_template_message(
        phone=phone,
        template_name=TEMPLATE_CORRECTION_REQ_V1,
        parameters=params
    )

def send_correction_done_v1(phone: str, full_name: str) -> Dict[str, Any]:
    """
    Sends 'correction_done_v1' template.
    Variable: {{1}}=Name
    """
    params = [full_name or "Brother/Sister"]
    return _send_template_message(
        phone=phone,
        template_name=TEMPLATE_CORRECTION_DONE_V1,
        parameters=params
    )
