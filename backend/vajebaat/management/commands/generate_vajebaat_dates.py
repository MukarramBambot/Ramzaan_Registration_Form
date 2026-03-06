from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from vajebaat.models import VajebaatDate, VajebaatSlot, DEFAULT_SLOT_TIMES

class Command(BaseCommand):
    help = 'Generates Vajebaat appointment dates and slots for a given range.'

    def add_arguments(self, parser):
        parser.add_argument('--start', type=str, help='Start date (YYYY-MM-DD)', default='2026-03-05')
        parser.add_argument('--end', type=str, help='End date (YYYY-MM-DD)', default='2026-03-18')

    def handle(self, *args, **options):
        try:
            start_date = date.fromisoformat(options['start'])
            end_date = date.fromisoformat(options['end'])
        except ValueError:
            self.stderr.write(self.style.ERROR('Invalid date format. Use YYYY-MM-DD.'))
            return

        if start_date > end_date:
            self.stderr.write(self.style.ERROR('Start date must be before end date.'))
            return

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
                    self.stdout.write(f'  Slot {num} exists')

            current_date += timedelta(days=1)
        
        self.stdout.write(self.style.SUCCESS('Successfully generated Vajebaat dates and slots.'))
