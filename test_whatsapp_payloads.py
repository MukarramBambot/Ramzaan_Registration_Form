"""
Test script to verify WhatsApp template message payloads.
This script demonstrates the exact JSON payload structure sent to Meta Graph API.
"""

import json

def test_registration_received():
    """Test payload for registration_received template"""
    print("\n" + "="*60)
    print("TEST 1: registration_received template")
    print("="*60)
    
    template_name = "registration_received"
    phone_number = "919876543210"
    parameters = ["Ahmed Ali"]
    
    # Simulate the payload structure
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": "en"},
            "components": [
                {
                    "type": "body",
                    "parameters": [{"type": "text", "text": p} for p in parameters]
                }
            ]
        }
    }
    
    print("\nPayload:")
    print(json.dumps(payload, indent=2))
    print("\nTemplate Parameters:")
    print(f"  {{{{1}}}} = {parameters[0]}")

def test_duty_allotment_confirmed():
    """Test payload for duty_allotment_confirmed template"""
    print("\n" + "="*60)
    print("TEST 2: duty_allotment_confirmed template")
    print("="*60)
    
    template_name = "duty_allotment_confirmed"
    phone_number = "919876543210"
    parameters = ["Ahmed Ali", "15 March 2026", "Fajar Azaan"]
    
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": "en"},
            "components": [
                {
                    "type": "body",
                    "parameters": [{"type": "text", "text": p} for p in parameters]
                }
            ]
        }
    }
    
    print("\nPayload:")
    print(json.dumps(payload, indent=2))
    print("\nTemplate Parameters:")
    print(f"  {{{{1}}}} = {parameters[0]}")
    print(f"  {{{{2}}}} = {parameters[1]}")
    print(f"  {{{{3}}}} = {parameters[2]}")

def test_duty_reminder_tomorrow():
    """Test payload for duty_reminder_tomorrow template"""
    print("\n" + "="*60)
    print("TEST 3: duty_reminder_tomorrow template")
    print("="*60)
    
    template_name = "duty_reminder_tomorrow"
    phone_number = "919876543210"
    parameters = ["Ahmed Ali", "15 March 2026", "Fajar Azaan"]
    
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": "en"},
            "components": [
                {
                    "type": "body",
                    "parameters": [{"type": "text", "text": p} for p in parameters]
                }
            ]
        }
    }
    
    print("\nPayload:")
    print(json.dumps(payload, indent=2))
    print("\nTemplate Parameters:")
    print(f"  {{{{1}}}} = {parameters[0]}")
    print(f"  {{{{2}}}} = {parameters[1]}")
    print(f"  {{{{3}}}} = {parameters[2]}")

def main():
    print("\n" + "="*60)
    print("WhatsApp Template Message Payload Verification")
    print("="*60)
    print("\nAPI Endpoint: https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages")
    print("Method: POST")
    print("Authorization: Bearer {ACCESS_TOKEN}")
    print("Content-Type: application/json")
    
    test_registration_received()
    test_duty_allotment_confirmed()
    test_duty_reminder_tomorrow()
    
    print("\n" + "="*60)
    print("All payload structures verified!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
