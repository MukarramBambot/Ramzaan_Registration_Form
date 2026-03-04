from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta, time
from vajebaat.models import VajebaatDate, VajebaatSlot, DEFAULT_SLOT_TIMES

class Command(BaseCommand):
    help = 'Populates Vajebaat dates and slots for March 1 - March 18, 2026'

    def handle(self, *args, **options):
        start_date = date(2026, 3, 1)
        end_date = date(2026, 3, 18)
        
        current_date = start_date
        while current_date <= end_date:
            # 1. Get or create the date
            date_obj, created = VajebaatDate.objects.get_or_create(date=current_date)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created date: {current_date}'))
            else:
                self.stdout.write(f'Date already exists: {current_date}')
            
            # 2. Ensure all 8 slots exist (idempotent)
            # The model has a signal that creates slots on 'created=True', 
            # but we explicitly check here for existing dates as well.
            for num, start, end in DEFAULT_SLOT_TIMES:
                slot_obj, s_created = VajebaatSlot.objects.get_or_create(
                    date=date_obj,
                    slot_number=num,
                    defaults={
                        'start_time': start,
                        'end_time': end,
                        'capacity': 10
                    }
                )
                if s_created:
                    self.stdout.write(f'  Created slot {num} ({start.strftime("%H:%M")})')
                else:
                    # Update capacity if it changed or ensure it is 10
                    if slot_obj.capacity != 10:
                        slot_obj.capacity = 10
                        slot_obj.save(update_fields=['capacity'])
                        self.stdout.write(f'  Updated slot {num} capacity to 10')

            current_date += timedelta(days=1)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated Vajebaat dates and slots.'))
