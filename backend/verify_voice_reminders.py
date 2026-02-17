import os
import django
import pytz
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sherullah_service.settings')
django.setup()

from registrations.models import Registration, DutyAssignment, DutyReminderCall
from registrations.tasks import schedule_voice_reminder_task

def verify_scheduling():
    print("--- Timezone & Scheduling Verification ---")
    
    # Get a dummy or existing test user
    reg = Registration.objects.first()
    if not reg:
        print("No registration found to test with.")
        return

    # Create a test assignment
    assignment = DutyAssignment.objects.create(
        assigned_user=reg,
        duty_date=datetime.now().date() + timedelta(days=1),
        namaaz_type='FAJAR_AZAAN' # Reporting time according to rules: 05:20 AM
    )
    print(f"Created Test Assignment: {assignment.id} for {reg.its_number}")

    # Trigger scheduling task
    print("Triggering schedule_voice_reminder_task...")
    schedule_voice_reminder_task(assignment.id)

    # Check for created reminder
    reminder = DutyReminderCall.objects.filter(duty_assignment=assignment).first()
    if reminder:
        print(f"Reminder created: ID {reminder.id}")
        print(f"Scheduled Time (UTC): {reminder.scheduled_time}")
        
        # Expected reporting: 05:20 AM IST
        # Scheduled: 03:20 AM IST
        # 03:20 AM IST is 21:50 PM UTC (of previous day) or something similar depending on date.
        
        ist = pytz.timezone('Asia/Kolkata')
        scheduled_ist = reminder.scheduled_time.astimezone(ist)
        print(f"Scheduled Time (IST): {scheduled_ist}")
        
        # Check if it's correct
        # Namaaz Rule FAJAR_AZAAN -> 05:20 AM
        # Scheduled -> 03:20 AM IST
        if scheduled_ist.hour == 3 and scheduled_ist.minute == 20:
            print("✓ Timezone conversion logic is CORRECT.")
        else:
            print(f"❌ Unexpected scheduled time: {scheduled_ist}")
            
    else:
        print("❌ Reminder NOT created!")

    print("\n--- Duplicate Protection Verification ---")
    # Trigger again
    print("Triggering schedule_voice_reminder_task again...")
    schedule_voice_reminder_task(assignment.id)
    
    count = DutyReminderCall.objects.filter(duty_assignment=assignment).count()
    if count == 1:
        print("✓ Duplicate protection works (Count=1).")
    else:
        print(f"❌ Duplicate protection FAILED (Count={count}).")

    # Cleanup test data
    # reminder.delete()
    # assignment.delete()
    # print("Test data cleaned up.")

if __name__ == "__main__":
    verify_scheduling()
