import sys
import os

# Add backend to path to find registrations module
sys.path.append('/var/www/Ramzaan_Registration_Form/backend')

# Import the function directly
# We mock the assignment object, so we don't need Django models
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
    ("ASAR_AZAAN", "12:30 PM"),
    ("ASAR_TAKBIRA", "12:30 PM"),
    ("MAGRIB_AZAAN", "05:40 PM"),
    ("ISHA_TAKBIRA", "05:40 PM"),
    ("UNKNOWN_DUTY", None),
]

print("Verifying Reporting Time Logic (Standalone)...\n")

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
    exit(1)
