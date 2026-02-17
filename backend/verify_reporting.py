import os
import django
import sys

# Setup Django environment
sys.path.append('/var/www/Ramzaan_Registration_Form/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sherullah_service.settings')
django.setup()

from registrations.utils.reporting import get_reporting_time
from collections import namedtuple

# Mock DutyAssignment
DutyAssignment = namedtuple('DutyAssignment', ['namaaz_type'])

test_cases = [
    ("SANAH", "04:30 AM"),
    ("TAJWEED", "04:30 AM"),
    ("FAJAR_AZAAN", "05:20 AM"),
    ("FAJAR_TAKBIRA", "05:20 AM"),
    ("ZOHAR_AZAAN", "12:30 PM"),
    ("ZOHR_TAKBIRA", "12:30 PM"),
    ("ASAR_AZAAN", "12:30 PM"), # Assuming ASAR also follows ZOHR timing if it existed? Wait, logic says zohr/asar -> 12:30
    ("ASAR_TAKBIRA", "12:30 PM"),
    ("MAGRIB_AZAAN", "05:40 PM"),
    ("ISHAA_TAKBIRA", "05:40 PM"),
    ("UNKNOWN_DUTY", None),
]

print("Verifying Reporting Time Logic...\n")

all_passed = True
for duty_type, expected in test_cases:
    assignment = DutyAssignment(namaaz_type=duty_type)
    result = get_reporting_time(assignment)
    
    status = "✅ PASS" if result == expected else f"❌ FAIL (Expected {expected}, got {result})"
    if result != expected:
        all_passed = False
    
    print(f"{duty_type:<15} -> {str(result):<10} {status}")

if all_passed:
    print("\nAll tests passed!")
else:
    print("\nSome tests failed.")
