
import os
import sys
import django

# Set up Django environment
sys.path.append('/var/www/Ramzaan_Registration_Form/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sherullah_service.settings')
django.setup()

from registrations.google_sheets import sync_all_to_sheets, sync_registration_to_sheets
from registrations.models import Registration

print("--- STARTING GSYNC VERIFICATION ---")

# Step 1: Bulk Sync Test
print("\n[Phase 1] Triggering Bulk Sync...")
success, count = sync_all_to_sheets()
print(f"Bulk Sync Result: Success={success}, Count={count}")

# Step 2: Single Sync Test (if data exists)
reg = Registration.objects.first()
if reg:
    print(f"\n[Phase 2] Triggering Single Sync for record: {reg.its_number}")
    sync_registration_to_sheets(reg)
# Step 3: Dummy Formula Test
print("\n[Phase 3] Triggering Dummy Formula Test...")
class DummyReg:
    def __init__(self):
        self.full_name = "Formula Test"
        self.its_number = "99999999"
        self.email = "test@example.com"
        self.phone_number = "1234567890"
        self.created_at = django.utils.timezone.now()
        self.status = "PENDING"
    def get_preference_display(self): return "Formula"
    def get_status_display(self): return "Formula"
    @property
    def audition_files(self):
        class DummyFiles:
            def first(self): return None
        return DummyFiles()

dummy_reg = DummyReg()
# Manually override prepare_row_data logic for dummy test
import registrations.google_sheets as gs
original_prepare = gs.prepare_row_data
try:
    gs.prepare_row_data = lambda r: [r.full_name, r.its_number, r.email, r.phone_number, "Formula", r.created_at.strftime('%Y-%m-%d %H:%M:%S'), "=1+1", "Formula"]
    gs.sync_registration_to_sheets(dummy_reg)
finally:
    gs.prepare_row_data = original_prepare

print("\n--- VERIFICATION FINISHED ---")
