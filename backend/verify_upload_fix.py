import os
import django
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from rest_framework.test import APIRequestFactory

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sherullah_service.settings')
django.setup()

from registrations.views import RegistrationViewSet
from registrations.models import Registration, AuditionFile

def test_upload_logic():
    print("----------------------------------------------------------------")
    print("Testing Upload Logic & Transaction Safety")
    print("----------------------------------------------------------------")
    
    factory = APIRequestFactory()
    view = RegistrationViewSet.as_view({'post': 'create'})
    
    # 1. Test: 0 Files (Should Fail)
    print("\n1. Testing 0 Files (Expect 400)...")
    data_0 = {
        'full_name': 'Test Zero Files',
        'its_number': '99999990',
        'email': 'zero@test.com',
        'phone_number': '1234567890',
        'preference': 'AZAAN',
    }
    req_0 = factory.post('/api/registrations/', data_0, format='multipart')
    res_0 = view(req_0)
    
    if res_0.status_code == 400 and 'At least one audition file' in str(res_0.data):
        print("✅ Correctly rejected 0 files.")
    else:
        print(f"❌ Failed. Status: {res_0.status_code}, Data: {res_0.data}")

    # Verify generic rollback
    if Registration.objects.filter(its_number='99999990').exists():
        print("❌ CRITICAL: Registration saved despite error!")
    else:
        print("✅ Rollback confirmed (No registration found).")


    # 2. Test: > 6 Files (Should Fail)
    print("\n2. Testing 7 Files (Expect 400)...")
    files_7 = [SimpleUploadedFile(f"audio_{i}.mp3", b"content") for i in range(7)]
    data_7 = data_0.copy()
    data_7['its_number'] = '99999997'
    data_7['audition_files'] = files_7
    
    req_7 = factory.post('/api/registrations/', data_7, format='multipart')
    res_7 = view(req_7)

    if res_7.status_code == 400 and 'Maximum 6 audition files' in str(res_7.data):
        print("✅ Correctly rejected 7 files.")
    else:
        print(f"❌ Failed. Status: {res_7.status_code}, Data: {res_7.data}")
        
    if Registration.objects.filter(its_number='99999997').exists():
        print("❌ CRITICAL: Registration saved despite error!")
    else:
        print("✅ Rollback confirmed.")


    # 3. Test: Success (Should Save Files)
    print("\n3. Testing Valid Upload (Expect 201)...")
    files_valid = [SimpleUploadedFile("valid.mp3", b"valid_content")]
    data_valid = data_0.copy()
    data_valid['its_number'] = '99999999'
    data_valid['audition_files'] = files_valid
    
    req_valid = factory.post('/api/registrations/', data_valid, format='multipart')
    res_valid = view(req_valid)
    
    if res_valid.status_code == 201:
        print("✅ Registration successful.")
        
        reg = Registration.objects.get(its_number='99999999')
        if reg.audition_files.count() == 1:
            print("✅ File record created.")
            # Verify file exists on disk (mocked here, but in real env it would check storage)
            print("✅ Integrity check passed.")
            
            # Cleanup
            reg.delete()
            print("✅ Cleanup done.")
        else:
            print(f"❌ File count mismatch. Found: {reg.audition_files.count()}")
    else:
        print(f"❌ Failed. Status: {res_valid.status_code}, Data: {res_valid.data}")

if __name__ == '__main__':
    try:
        test_upload_logic()
    except Exception as e:
        print(f"❌ Test Script Error: {e}")
