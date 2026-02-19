import requests
import sys

BASE_URL = "http://localhost:8000/api/registrations/"

def test_registration_no_files():
    print("Testing registration WITHOUT files...")
    data = {
        "full_name": "Test User No Files",
        "its_number": "12345678",
        "email": "testnofiles@example.com",
        "phone_number": "919999999999",
        "preference": ["AZAAN"]
    }
    
    # Use multipart/form-data as the backend expects it
    response = requests.post(BASE_URL, data=data)
    
    if response.status_code == 201:
        print("✅ SUCCESS: Registration created without files.")
        return response.json()['id']
    else:
        print(f"❌ FAILED: Status code {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_registration_with_files():
    print("\nTesting registration WITH files...")
    data = {
        "full_name": "Test User With Files",
        "its_number": "87654321",
        "email": "testwithfiles@example.com",
        "phone_number": "918888888888",
        "preference": ["TAKHBIRA"]
    }
    
    # Create a dummy file
    files = [
        ('audition_files', ('test_audio.mp3', b'fake audio data', 'audio/mpeg'))
    ]
    
    response = requests.post(BASE_URL, data=data, files=files)
    
    if response.status_code == 201:
        print("✅ SUCCESS: Registration created with files.")
        return response.json()['id']
    else:
        print(f"❌ FAILED: Status code {response.status_code}")
        print(f"Response: {response.text}")
        return None

if __name__ == "__main__":
    reg_id_1 = test_registration_no_files()
    reg_id_2 = test_registration_with_files()
    
    if reg_id_1 and reg_id_2:
        print("\nVerification complete: Both cases passed.")
        sys.exit(0)
    else:
        print("\nVerification failed.")
        sys.exit(1)
