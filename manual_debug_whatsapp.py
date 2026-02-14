
import os
import requests
import json
import logging
from dotenv import load_dotenv

# Setup basic logging to console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load .env variables
load_dotenv()

def debug_whatsapp_send():
    print("----------------------------------------------------------------")
    print("   WHATSAPP CLOUD API - STANDALONE DEBUGGER")
    print("----------------------------------------------------------------")

    # 1. Load Credentials
    phone_id = os.getenv("META_WA_PHONE_NUMBER_ID")
    access_token = os.getenv("META_WA_ACCESS_TOKEN")
    current_version = os.getenv("META_WA_API_VERSION", "v18.0") # Default fallback

    print(f"[*] Phone Number ID: {phone_id}")
    print(f"[*] API Version: {current_version}")
    print(f"[*] Access Token Status: {'PRESENT' if access_token else 'MISSING'}")

    if not phone_id or not access_token:
        print("[!] Error: Missing credentials in .env file.")
        return

    # 2. Ask user for target info
    print("\nNote: Ensure the target number is registered on WhatsApp.")
    recipient = input("Enter Recipient Phone Number (e.g., 919876543210): ").strip()
    template_name = input("Enter Template Name (default: registration_received): ").strip() or "registration_received"
    
    # 3. Construct URL - FORCE v20.0 or v19.0 if current_version looks wrong
    # The user has v24.0 in .env which is likely invalid.
    # We will try with the env version first, but warn.
    target_version = current_version
    if "v24" in current_version:
        print(f"[!] Warning: {current_version} seems too high. Meta current version is typically v19.0-v21.0.")
        print("[!] I will attempt using 'v20.0' instead for safety.")
        target_version = "v20.0"

    url = f"https://graph.facebook.com/{target_version}/{phone_id}/messages"
    
    # 4. Prepare Payload
    # Using 'registration_received' structure (1 variable)
    # Using 'duty_allotment_confirmed' structure (3 variables)
    
    components = []
    
    if template_name == "duty_allotment_confirmed":
        print("\nUsing 3 dummy parameters for duty allotment...")
        params = [
            {"type": "text", "text": "Debug User"},
            {"type": "text", "text": "01 Jan 2025"},
            {"type": "text", "text": "TEST SLOT"}
        ]
    else:
        print("\nUsing 1 dummy parameter for standard template...")
        params = [
            {"type": "text", "text": "Debug User"}
        ]

    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": "en"  # Try 'en' first. If fails, try 'en_US' manually
            },
            "components": [
                {
                    "type": "body",
                    "parameters": params
                }
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    print(f"\n[*] Sending Request to: {url}")
    print(f"[*] Payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        
        print("\n---------------- RESPONSE ----------------")
        print(f"Status Code: {response.status_code}")
        
        try:
            res_data = response.json()
            print(json.dumps(res_data, indent=2))
        except:
            print("Raw Text:", response.text)

        if response.status_code == 200:
            print("\n[SUCCESS] Message Sent!")
        else:
            print("\n[FAILURE] Meta API returned an error.")
            
    except Exception as e:
        print(f"\n[EXCEPTION] Network/Script Error: {e}")

if __name__ == "__main__":
    debug_whatsapp_send()
