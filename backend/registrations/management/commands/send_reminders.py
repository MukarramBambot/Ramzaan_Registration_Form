from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from registrations.models import Slot
from registrations.utils.whatsapp import send_event_reminder_24hrs
from registrations.utils.email_notifications import send_reminder_email

class Command(BaseCommand):
    help = 'Sends reminders for slots scheduled for tomorrow.'

    def handle(self, *args, **options):
        self.stdout.write("Checking for reminders...")
        
        tomorrow = timezone.now().date() + timedelta(days=1)
        slots = Slot.objects.filter(date=tomorrow)
        
        if not slots.exists():
            self.stdout.write(f"No slots found for tomorrow ({tomorrow}).")
            return

        self.stdout.write(f"Found {slots.count()} slots for {tomorrow}.")
        
        for slot in slots:
            reg = slot.registration
            
            # 1. Send Email (New Service)
            if reg.email:
                # Format date: 12 March 2026
                # Note: send_reminder_email handles date formatting inside if we pass object, 
                # but design said args are (registration, date, time).
                # Let's check email_notifications.py... 
                # def send_reminder_email(registration, date_str, time_str):
                
                date_str = slot.date.strftime('%d %B %Y')
                send_reminder_email(reg, date_str, slot.time_label)
            
            # 2. Send WhatsApp (Template)
            if reg.phone_number:
                # Format date: 12 March 2026
                date_str = slot.date.strftime('%d %B %Y')
                send_event_reminder_24hrs(reg, date_str, slot.time_label)
                
            self.stdout.write(f"Reminders sent for {reg.full_name}")

        self.stdout.write(self.style.SUCCESS("All reminders processed."))
