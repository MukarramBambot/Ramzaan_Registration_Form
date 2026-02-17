import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sherullah_service.settings')
django.setup()

from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from registrations.models import Registration, RegistrationCorrection
from registrations.views import CorrectionViewSet
from registrations.serializers import RegistrationCorrectionSerializer

def test_correction_workflow():
    print("----------------------------------------------------------------")
    print("Testing Correction Workflow")
    print("----------------------------------------------------------------")
    
    # 1. Setup Data
    user, _ = User.objects.get_or_create(username='admin_test', is_staff=True, is_superuser=True)
    
    reg = Registration.objects.create(
        full_name='Correction Test',
        its_number='88888888',
        email='correction@test.com',
        phone_number='1234567890',
        preference=['AZAAN']
    )
    print(f"✅ Created Registration: {reg.id}")

    factory = APIRequestFactory()
    view = CorrectionViewSet.as_view({'post': 'create', 'get': 'retrieve_by_token'})
    resolve_view = CorrectionViewSet.as_view({'post': 'resolve_by_token'})

    # 2. Admin Requests Correction
    print("\n1. Admin Requesting Correction...")
    data = {
        'registration': reg.id,
        'field_name': 'full_name',
        'admin_message': 'Please fix your name spelling.'
    }
    request = factory.post('/api/corrections/', data)
    force_authenticate(request, user=user)
    response = view(request)
    
    if response.status_code == 201:
        print("✅ Correction Created.")
        token = response.data['token']
        print(f"   Token: {token}")
    else:
        print(f"❌ Failed to create correction: {response.data}")
        return

    # 3. Public Retrieve Correction
    print("\n2. Public Retrieving Correction...")
    request = factory.get(f'/api/corrections/token/{token}/')
    response = view(request, token=token)
    
    if response.status_code == 200:
        print(f"✅ Retrieved: {response.data['field_name']} - {response.data['admin_message']}")
    else:
        print(f"❌ Failed to retrieve: {response.data}")
        return

    # 4. Public Resolve Correction
    print("\n3. Public Resolving Correction...")
    data = {
        'full_name': 'Correction Tested Updated'
    }
    request = factory.post(f'/api/corrections/resolve/{token}/', data)
    response = resolve_view(request, token=token)
    
    if response.status_code == 200:
        print("✅ Correction Resolved (Status 200).")
    else:
        print(f"❌ Failed to resolve: {response.data}")
        return

    # 5. Verify Database
    reg.refresh_from_db()
    correction = RegistrationCorrection.objects.get(token=token)
    
    if reg.full_name == 'Correction Tested Updated':
        print("✅ Registration Field Updated.")
    else:
        print(f"❌ Registration Field NOT Updated. Found: {reg.full_name}")

    if correction.status == 'RESOLVED':
        print("✅ Correction Status RESOLVED.")
    else:
        print(f"❌ Correction Status NOT Updated. Found: {correction.status}")

    # Cleanup
    reg.delete()
    print("\n✅ Cleanup Done.")

if __name__ == '__main__':
    try:
        test_correction_workflow()
    except Exception as e:
        print(f"❌ Test Script Error: {e}")
