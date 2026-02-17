import os
import django
import sys
from datetime import date

# Setup Django environment
sys.path.append('/var/www/Ramzaan_Registration_Form/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sherullah_service.settings')
django.setup()

from registrations.models import DutyAssignment, Registration

def verify_choices():
    choices = dict(DutyAssignment.NAMAAZ_CHOICES)
    new_keys = ['SANAH', 'TAJWEED', 'DUA_E_JOSHAN', 'YASEEN']
    
    print("Verifying Duty Assignment Choices...")
    all_present = True
    for key in new_keys:
        if key in choices:
            print(f"✅ {key} is present.")
        else:
            print(f"❌ {key} is MISSING.")
            all_present = False
            
    return all_present

def clean_test_data():
    try:
        DutyAssignment.objects.filter(duty_date=date(2026, 2, 17), namaaz_type='SANAH').delete()
        print("Cleaned up previous test data.")
    except Exception as e:
        print(f"Cleanup error: {e}")

def verify_assignment_creation():
    print("\nVerifying Assignment Creation for SANAH...")
    try:
        # Get a random user or create one
        user, created = Registration.objects.get_or_create(
            its_number='99999999',
            defaults={
                'full_name': 'Test User',
                'email': 'test@example.com',
                'phone_number': '1234567890'
            }
        )
        
        assignment = DutyAssignment.objects.create(
            duty_date=date(2026, 2, 17),
            namaaz_type='SANAH',
            assigned_user=user
        )
        print(f"✅ Successfully created assignment: {assignment}")
        
        # Verify persistence
        exists = DutyAssignment.objects.filter(duty_date=date(2026, 2, 17), namaaz_type='SANAH').exists()
        if exists:
            print(f"✅ Assignment persists in DB.")
        else:
            print(f"❌ Assignment NOT found in DB after creation.")
            
        return True

    except Exception as e:
        print(f"❌ Failed to create assignment: {e}")
        return False
    finally:
        # cleanup
        clean_test_data()

if __name__ == "__main__":
    scan_ok = verify_choices()
    creation_ok = verify_assignment_creation()
    
    if scan_ok and creation_ok:
        print("\nAll Backend Checks Passed!")
    else:
        print("\nBackend Checks Failed.")
        exit(1)
