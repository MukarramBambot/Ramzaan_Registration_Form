"""
Management command to test Twilio WhatsApp integration.
Usage: python manage.py test_twilio_whatsapp <phone_number>
Example: python manage.py test_twilio_whatsapp 919876543210
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from registrations.utils.whatsapp import send_whatsapp_message
import logging

logger = logging.getLogger('registrations')


class Command(BaseCommand):
    help = 'Test Twilio WhatsApp integration by sending a test message'

    def add_arguments(self, parser):
        parser.add_argument(
            'phone_number',
            type=str,
            help='Phone number to send test message to (e.g., 919876543210 or +919876543210)'
        )

    def handle(self, *args, **options):
        phone_number = options['phone_number']
        
        # Check Twilio credentials
        account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
        twilio_from = getattr(settings, 'TWILIO_WHATSAPP_FROM', '')
        
        if not all([account_sid, auth_token, twilio_from]):
            self.stdout.write(
                self.style.ERROR(
                    '❌ Twilio credentials not configured:\n'
                    f'   TWILIO_ACCOUNT_SID: {bool(account_sid)}\n'
                    f'   TWILIO_AUTH_TOKEN: {bool(auth_token)}\n'
                    f'   TWILIO_WHATSAPP_FROM: {bool(twilio_from)}'
                )
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Twilio credentials found\n'
                f'   Using From: {twilio_from}'
            )
        )
        
        # Send test message
        test_message = (
            "Assalamu Alaikum 👋\n\n"
            "This is a test message from Sherullah Portal WhatsApp integration.\n\n"
            "If you receive this, Twilio WhatsApp is working correctly! ✅\n\n"
            "JazakAllah Khair."
        )
        
        self.stdout.write(
            f'\n📱 Sending test message to: {phone_number}\n'
            f'📝 Message preview: {test_message[:50]}...\n'
        )
        
        result = send_whatsapp_message(phone_number, test_message)
        
        # Handle response
        if result == True:
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Message sent successfully!\n'
                    f'   Status: SUCCESS (SID returned from Twilio)'
                )
            )
        elif result == "SANDBOX":
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️  Sandbox restriction:\n'
                    f'   The phone number {phone_number} is not in the Twilio sandbox.\n'
                    f'   To send messages, whitelist this number in Twilio Console:\n'
                    f'   https://console.twilio.com/us/account/messaging/services\n'
                    f'   Then re-run this command.'
                )
            )
        elif result == False:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Message failed to send.\n'
                    f'   Check logs at: backend/logs/django.log'
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Unexpected result: {result}\n'
                    f'   Check logs at: backend/logs/django.log'
                )
            )
