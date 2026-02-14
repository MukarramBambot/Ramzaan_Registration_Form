from django.core.management.base import BaseCommand
from registrations.models import Registration
from registrations.utils.whatsapp import send_registration_notification
import logging

class Command(BaseCommand):
    help = 'Tests Meta WhatsApp Cloud API integration by sending a registration notification.'

    def add_arguments(self, parser):
        parser.add_argument('phone', type=str, help='Recipient phone number')
        parser.add_argument('--name', type=str, default='Test User', help='Internal name for testing')

    def handle(self, *args, **options):
        self.stdout.write(f"Testing Meta WhatsApp for {options['phone']}...")
        
        # Create a mock objects for the utility
        class MockRegistration:
            def __init__(self, name, phone):
                self.full_name = name
                self.phone_number = phone
        
        mock_reg = MockRegistration(options['name'], options['phone'])
        
        success = send_registration_notification(mock_reg)
        
        if success:
            self.stdout.write(self.style.SUCCESS("✓ WhatsApp delivery attempt triggered (check logs for Meta ID)"))
        else:
            self.stdout.write(self.style.ERROR("⨯ WhatsApp delivery failed (check logs for API error)"))
