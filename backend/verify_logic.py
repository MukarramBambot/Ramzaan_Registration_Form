from collections import namedtuple

# Copy of the function from registrations/utils/reporting.py
def get_reporting_time(assignment):
    """
    Returns the reporting time string based on the assignment's namaaz_type.
    """
    pre_fajr_khidmat = [
        "SANAH",
        "TAJWEED",
        "DUA_E_JOSHAN",
        "YASEEN",
        "JOSHAN",
        "TILAWAT",
    ]

    # Normalize to upper case just in case
    namaaz_type = assignment.namaaz_type.upper()

    if namaaz_type in pre_fajr_khidmat:
        return "04:30 AM"

    if namaaz_type in ["FAJAR_AZAAN", "FAJAR_TAKBIRA"]:
        return "05:20 AM"

    if namaaz_type in [
        "ZOHR_AZAAN", "ZOHAR_AZAAN",
        "ZOHR_TAKBIRA", "ZOHAR_TAKBIRA",
        "ASHAR_AZAAN", "ASAR_AZAAN",
        "ASHAR_TAKBIRA", "ASAR_TAKBIRA"
    ]:
        return "12:30 PM"

    if namaaz_type in [
        "MAGRIB_AZAAN",
        "MAGRIB_TAKBIRA",
        "ISHA_AZAAN", "ISHAA_AZAAN",
        "ISHA_TAKBIRA", "ISHAA_TAKBIRA"
    ]:
        return "05:40 PM"

    return None

# Verify Logic
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
    ("ISHAA_TAKBIRA", "05:40 PM"),
    ("UNKNOWN_DUTY", None),
]

print("Verifying Reporting Time Logic (Copy)...\n")

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
