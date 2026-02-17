import requests
import os
import logging
from requests.auth import HTTPBasicAuth

# Voice reminder system isolated from core registration logic.
# Failure here must never affect registration or allotment.

logger = logging.getLogger('registrations')

def make_exotel_call(registration, assignment, reporting_time_str):
    """
    Triggers an Exotel Voice Flow call.
    
    Variables passed to Flow:
    - name: User Full Name
    - duty_name: Duty Display Name
    - duty_date: Date of duty (DD/MM/YYYY)
    - reporting_time: Human readable reporting time
    """
    
    sid = os.getenv('EXOTEL_SID')
    api_key = os.getenv('EXOTEL_API_KEY')
    api_token = os.getenv('EXOTEL_API_TOKEN')
    caller_id = os.getenv('EXOTEL_CALLER_ID')
    flow_id = os.getenv('EXOTEL_FLOW_ID')
    
    if not all([sid, api_key, api_token, caller_id, flow_id]):
        logger.error("[Exotel] Missing environment variables for call")
        return {"success": False, "error": "Missing credentials"}

    url = f"https://api.exotel.com/v1/Accounts/{sid}/Calls/connect.json"
    
    # Custom Field for Exotel Flow variables
    # Exotel expects variables in specific format if using specialized flow features, 
    # but usually CustomField is used to pass data to the flow.
    # Format: Var1=Val1&Var2=Val2
    
    duty_name = assignment.get_namaaz_type_display()
    duty_date = assignment.duty_date.strftime('%d/%m/%Y')
    
    # Note: Exotel variables often need to be URL encoded within the CustomField
    custom_field = f"name={registration.full_name}&duty_name={duty_name}&duty_date={duty_date}&reporting_time={reporting_time_str}"
    
    payload = {
        'From': registration.phone_number,
        'To': registration.phone_number, # In Connect API 'From' is destination if 'To' is Flow, but Exotel V1 'From' is Customer, 'To' is Flow?
        # Actually for 'connect.json' to a Flow:
        # 'From': Customer Number
        # 'To': Customer Number (Wait, usually 'From' is Caller ID, 'To' is Customer)
        # Checking Exotel V1 Docs:
        # From: The phone number of the person who will receive the call first. 
        # To: The phone number (or Flow ID) of the person (or app) who will receive the call next.
        # FlowId: The ID of the flow you want to connect the call to.
        
        'From': registration.phone_number,
        'CallerId': caller_id,
        'Url': f"http://my.exotel.com/{sid}/examl/start_voice/{flow_id}", # Or use FlowId parameter if supported by account
        'CustomField': custom_field
    }

    # If your account prefers FlowId directly:
    # payload['FlowId'] = flow_id

    try:
        logger.info(f"[Exotel] Attempting call to {registration.phone_number} for {duty_name}")
        response = requests.post(
            url,
            auth=HTTPBasicAuth(api_key, api_token),
            data=payload,
            timeout=10
        )
        
        result = response.json()
        
        if response.status_code == 200:
            call_sid = result.get('Call', {}).get('Sid')
            logger.info(f"[Exotel] Call triggered successfully. Sid: {call_sid}")
            return {"success": True, "call_sid": call_sid}
        else:
            logger.error(f"[Exotel] API Error: {response.text}")
            return {"success": False, "error": response.text}
            
    except Exception as e:
        logger.error(f"[Exotel] Request failed: {str(e)}")
        return {"success": False, "error": str(e)}
