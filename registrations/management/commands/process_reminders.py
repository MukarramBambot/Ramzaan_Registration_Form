from django.core.management.base import BaseCommand
from registrations.utils import process_pending_reminders
import logging

logger = logging.getLogger('registrations')

class Command(BaseCommand):
    help = 'Processes pending email and WhatsApp reminders for duty assignments.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting reminder processing...'))
        try:
            stats = process_pending_reminders()
            self.stdout.write(self.style.SUCCESS(
                f"Successfully processed reminders.\n"
                f"Total Due: {stats['total_due']}\n"
                f"Emails Sent: {stats['email_success']}\n"
                f"WhatsApp Sent: {stats['whatsapp_success']}"
            ))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error processing reminders: {str(e)}"))
            logger.error(f"Management command process_reminders failed: {str(e)}")
