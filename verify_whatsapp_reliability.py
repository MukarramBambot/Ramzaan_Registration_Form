import os
import django
import json
import logging
from unittest.mock import MagicMock, patch

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sherullah_service.settings')
django.setup()

from registrations.utils.phone import normalize_phone_number
from registrations.utils.whatsapp import _send_template_message
from registrations.models import Registration
from registrations.webhook_views import whatsapp_webhook
from django.test import RequestFactory

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_phone_normalization():
    logger.info("--- Testing Phone Normalization ---")
    
    test_cases = [
        ("9876543210", "919876543210"),          # 10 digit -> add 91
        ("+91 98765 43210", "919876543210"),     # Format with space and +
        ("09876543210", "919876543210"),         # Leading zero
        ("919876543210", "919876543210"),        # Already normalized
        ("123", ValueError),                     # Too short
    ]
    
    for input_val, expected in test_cases:
        try:
            result = normalize_phone_number(input_val)
            if result == expected:
                logger.info(f"✓ '{input_val}' -> '{result}'")
            else:
                logger.error(f"✗ '{input_val}' -> '{result}' (Expected: {expected})")
        except ValueError:
            if expected is ValueError:
                logger.info(f"✓ '{input_val}' -> Error (Expected)")
            else:
                logger.error(f"✗ '{input_val}' -> Error (Unexpected)")

def test_whatsapp_api_structure():
    logger.info("\n--- Testing WhatsApp API Response Structure (Mocked) ---")
    
    # Mock requests.post
    with patch('requests.post') as mock_post:
        # Mock Success Response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "messaging_product": "whatsapp",
            "messages": [{"id": "wamid.TEST12345"}]
        }
        
        result = _send_template_message("9876543210", "test_template", ["param1"])
        
        if result['success'] and result['message_id'] == "wamid.TEST12345":
            logger.info("✓ Success Response Parsed Correctly")
        else:
            logger.error(f"✗ Success Response Failed: {result}")

        # Mock Failure Response
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {
            "error": {"message": "Invalid Parameter", "code": 100}
        }
        
        result_fail = _send_template_message("9876543210", "test_template", ["param1"])
        
        if not result_fail['success'] and result_fail['status_code'] == 400:
             logger.info("✓ Failure Response Parsed Correctly")
        else:
             logger.error(f"✗ Failure Response Failed: {result_fail}")

def test_webhook_processing():
    logger.info("\n--- Testing Webhook Processing ---")
    
    # Create valid registration
    reg = Registration.objects.create(
        full_name="Test User",
        its_number="12345678",
        email="test@example.com",
        phone_number="9876543210",
        preference="AZAAN",
        whatsapp_message_id="wamid.WEBHOOK_TEST"
    )
    
    # Simulate Webhook POST
    factory = RequestFactory()
    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "changes": [{
                "value": {
                    "statuses": [{
                        "id": "wamid.WEBHOOK_TEST",
                        "status": "delivered",
                        "timestamp": "1678900000"
                    }]
                }
            }]
        }]
    }
    
    request = factory.post(
        '/api/webhooks/whatsapp/', 
        data=json.dumps(payload), 
        content_type='application/json'
    )
    
    response = whatsapp_webhook(request)
    
    # Refresh DB
    reg.refresh_from_db()
    
    if response.status_code == 200 and reg.whatsapp_status == 'DELIVERED':
        logger.info(f"✓ Webhook Updated Status to DELIVERED")
    else:
        logger.error(f"✗ Webhook Failed. Status: {response.status_code}, DB Status: {reg.whatsapp_status}")
    
    # Cleanup
    reg.delete()

if __name__ == "__main__":
    test_phone_normalization()
    test_whatsapp_api_structure()
    test_webhook_processing()
