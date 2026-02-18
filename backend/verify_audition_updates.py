import os
import sys

# Setup Django before other imports
sys.path.append('/var/www/Ramzaan_Registration_Form/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sherullah_service.settings')

import django
django.setup()

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from rest_framework.test import APIRequestFactory
from registrations.views import RegistrationViewSet
from registrations.models import Registration, AuditionFile

def test_audition_updates():
    print("----------------------------------------------------------------")
    print("Testing Audition Updates (Optional Uploads, Max 6 Files, Audio Only)")
    print("----------------------------------------------------------------")
    
    factory = APIRequestFactory()
    view = RegistrationViewSet.as_view({'post': 'create'})
    
    base_data = {
        'full_name': 'Test Verification',
        'email': 'verify@test.com',
        'phone_number': '1234567890',
        'preference': 'AZAAN',
    }

    # 1. Test: 0 Files (Should Succeed now)
    print("\n1. Testing 0 Files (Expect 201)...")
    data_0 = base_data.copy()
    data_0['its_number'] = '10000000'
    req_0 = factory.post('/api/registrations/', data_0, format='multipart')
    res_0 = view(req_0)
    
    if res_0.status_code == 201:
        print("✅ Correctly accepted 0 files.")
        if Registration.objects.filter(its_number='10000000').exists():
            print("✅ Registration saved successfully.")
    else:
        print(f"❌ Failed. Status: {res_0.status_code}, Data: {res_0.data}")

    # 2. Test: 6 Files (Should Succeed)
    print("\n2. Testing 6 Files (Expect 201)...")
    files_6 = [SimpleUploadedFile(f"audio_{i}.mp3", b"content") for i in range(6)]
    data_6 = base_data.copy()
    data_6['its_number'] = '10000006'
    data_6['audition_files'] = files_6
    
    req_6 = factory.post('/api/registrations/', data_6, format='multipart')
    res_6 = view(req_6)

    if res_6.status_code == 201:
        print("✅ Correctly accepted 6 files.")
        reg = Registration.objects.get(its_number='10000006')
        if reg.audition_files.count() == 6:
            print(f"✅ Correctly saved {reg.audition_files.count()} files.")
    else:
        print(f"❌ Failed. Status: {res_6.status_code}, Data: {res_6.data}")

    # 3. Test: 7 Files (Should Fail)
    print("\n3. Testing 7 Files (Expect 400)...")
    files_7 = [SimpleUploadedFile(f"audio_{i}.mp3", b"content") for i in range(7)]
    data_7 = base_data.copy()
    data_7['its_number'] = '10000007'
    data_7['audition_files'] = files_7
    
    req_7 = factory.post('/api/registrations/', data_7, format='multipart')
    res_7 = view(req_7)

    if res_7.status_code == 400 and 'Maximum 6 audition files' in str(res_7.data):
        print("✅ Correctly rejected 7 files.")
    else:
        print(f"❌ Failed or returned unexpected status. Status: {res_7.status_code}, Data: {res_7.data}")
    
    if Registration.objects.filter(its_number='10000007').exists():
        print("❌ CRITICAL: Registration saved despite error!")

    # 4. Test: FLAC Format (Should Succeed)
    print("\n4. Testing FLAC format (Expect 201)...")
    files_flac = [SimpleUploadedFile("test.flac", b"flac_content")]
    data_flac = base_data.copy()
    data_flac['its_number'] = '10000188'
    data_flac['audition_files'] = files_flac
    
    req_flac = factory.post('/api/registrations/', data_flac, format='multipart')
    res_flac = view(req_flac)
    
    if res_flac.status_code == 201:
        print("✅ Correctly accepted FLAC file.")
    else:
        print(f"❌ Failed to accept FLAC. Status: {res_flac.status_code}, Data: {res_flac.data}")

    # Cleanup
    print("\nCleaning up test data...")
    Registration.objects.filter(its_number__startswith='1000').delete()
    print("✅ Cleanup complete.")

if __name__ == '__main__':
    try:
        test_audition_updates()
    except Exception as e:
        print(f"❌ Test Script Error: {e}")
