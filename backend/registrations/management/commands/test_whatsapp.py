from django.core.management.base import BaseCommand, CommandError
from registrations.utils.whatsapp import send_whatsapp_message

class Command(BaseCommand):
    help = 'Send a test WhatsApp message to the given phone number using production path.'

    def add_arguments(self, parser):
        parser.add_argument('phone', type=str, help='Phone number to send to (with country code)')
        parser.add_argument('--message', type=str, default=None, help='Optional message body')

    def handle(self, *args, **options):
        phone = options['phone']
        message = options['message'] or (
            "Assalamu Alaikum, this is a test message from Sherullah registration system."
        )

        self.stdout.write(f"Sending test WhatsApp to {phone}...")
        try:
            res = send_whatsapp_message(phone, message)
            if res is True:
                self.stdout.write(self.style.SUCCESS(f"Message sent to {phone}"))
            elif res == "SANDBOX":
                self.stdout.write(self.style.WARNING(f"Sandbox: recipient {phone} not in allowed list. Message skipped."))
            else:
                self.stdout.write(self.style.ERROR(f"Failed to send message to {phone}."))
        except Exception as e:
            raise CommandError(f"Unexpected error: {str(e)}")
