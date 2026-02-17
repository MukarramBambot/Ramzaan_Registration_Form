import os
import django
import sys
from django.db import transaction

# Setup Django environment
sys.path.append('/var/www/Ramzaan_Registration_Form/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sherullah_service.settings')
django.setup()

from registrations.models import Registration, AuditionFile
from rest_framework.test import APIRequestFactory, force_authenticate
from registrations.views import RegistrationViewSet, AuditionFileViewSet

from django.contrib.auth.models import User

def verify_backend_logic():
    print("----------------------------------------------------------------")
    print("Testing Audition Management Logic")
    print("----------------------------------------------------------------")

    # 1. Setup Test Data
    try:
        # Create Admin User for Auth
        admin_user, _ = User.objects.get_or_create(username='admin_test', defaults={'email': 'admin@test.com', 'is_staff': True})
        if not admin_user.is_staff:
            admin_user.is_staff = True
            admin_user.save()

        # Create Registration for Data
        reg, _ = Registration.objects.get_or_create(
            its_number='88888888',
            defaults={
                'full_name': 'Audition Test Candidate',
                'email': 'candidate@test.com',
                'phone_number': '1234567890'
            }
        )
        
        # Create 3 dummy audition files
        a1 = AuditionFile.objects.create(registration=reg, audition_display_name="File A", is_selected=False)
        a2 = AuditionFile.objects.create(registration=reg, audition_display_name="File B", is_selected=True) # Pre-selected to test switch
        a3 = AuditionFile.objects.create(registration=reg, audition_display_name="File C", is_selected=False)
        print(f"✅ Created test admin and registration with 3 files (IDs: {a1.id}, {a2.id}, {a3.id})")

        # 2. Test GET Auditions List
        print("\nTesting GET /api/registrations/{id}/auditions/...")
        factory = APIRequestFactory()
        view = RegistrationViewSet.as_view({'get': 'auditions'})
        request = factory.get(f'/api/registrations/{reg.id}/auditions/')
        force_authenticate(request, user=admin_user)
        response = view(request, pk=reg.id)
        
        if response.status_code == 200:
            print("✅ API returned 200 OK")
            data = response.data
            if len(data) == 3:
                print(f"✅ API returned 3 files.")
                # Verify is_selected
                selected = [f['id'] for f in data if f['is_selected']]
                if len(selected) == 1 and selected[0] == a2.id:
                     print(f"✅ Correct file marked as selected (ID: {a2.id})")
                else:
                     print(f"❌ Incorrect selection state: {selected}")
            else:
                print(f"❌ Expected 3 files, got {len(data)}")
        else:
            print(f"❌ API failed with {response.status_code}")

        # 3. Test PATCH Select Audition (Select A, should deselect B)
        print(f"\nTesting PATCH /api/audition-files/{a1.id}/select_audition/...")
        view_select = AuditionFileViewSet.as_view({'patch': 'select_audition'})
        request_select = factory.patch(f'/api/audition-files/{a1.id}/select_audition/')
        force_authenticate(request_select, user=admin_user)
        response_select = view_select(request_select, pk=a1.id)

        if response_select.status_code == 200:
             print("✅ API returned 200 OK")
             # Verify DB state
             a1.refresh_from_db()
             a2.refresh_from_db()
             a3.refresh_from_db()
             
             if a1.is_selected and not a2.is_selected and not a3.is_selected:
                 print("✅ Logic Correct: File A selected, File B deselected.")
             else:
                 print(f"❌ Logic Failed: A={a1.is_selected}, B={a2.is_selected}, C={a3.is_selected}")
        else:
             print(f"❌ API failed with {response_select.status_code}")
             print(response_select.data)

    except Exception as e:
        print(f"❌ Test Crash: {e}")
    finally:
        # Cleanup
        if 'reg' in locals():
            reg.audition_files.all().delete()
            reg.delete()
        if 'admin_user' in locals():
            admin_user.delete()
            print("\nCleaned up test data.")

if __name__ == "__main__":
    verify_backend_logic()
