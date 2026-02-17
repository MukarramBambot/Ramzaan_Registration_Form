def get_reporting_time(assignment):
    """
    Returns the reporting time string based on the assignment's namaaz type.
    
    Rules:
    - Pre-Fajr (Sanah, Tajweed, Joshan, Yaseen): 04:30 AM
    - Fajar (Azaan, Takbira): 05:20 AM
    - Zohr/Ashar (Azaan, Takbira): 12:30 PM
    - Magrib/Isha (Azaan, Takbira): 05:40 PM
    """
    
    pre_fajr_khidmat = [
        "SANAH",
        "TAJWEED",
        "DUA_E_JOSHAN",
        "YASEEN",
        "JOSHAN", # Added JOSHAN to match model choices
        "TILAWAT", # Added TILAWAT to match model choices
    ]

    # Normalize to upper case just in case, though model choices are upper
    namaaz_type = assignment.namaaz_type.upper()

    if namaaz_type in pre_fajr_khidmat:
        return "04:30 AM"

    if namaaz_type in ["FAJAR_AZAAN", "FAJAR_TAKBIRA"]:
        return "05:20 AM"

    if namaaz_type in [
        "ZOHR_AZAAN", "ZOHAR_AZAAN", # Handle potential spelling variations
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
