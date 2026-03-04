import requests
import time
import json

BASE_URL = "http://localhost:8000/api"
ADMIN_USER = "60451866"
ADMIN_PASS = "admin123" # Placeholder, assuming existing dev auth or bypass

# For local testing, we might need a token.
# Let's try to get a token if possible, or assume open for now if dev.
# In a real scenario, I'd login.
def get_admin_headers():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcyNjU2MDU2LCJpYXQiOjE3NzI2NTI0NTYsImp0aSI6IjZjMzZkNjcyZGEzZDRkYjA4NmI0OTIxODhiYTY1MTQ2IiwidXNlcl9pZCI6IjEifQ.rL78f59MYqI0Nbw18N2nUACO3C-XLUYz-lYGKgE-ZgI"
    return {"Authorization": f"Bearer {token}"}

HEADERS = get_admin_headers()

def check_status(name, resp, expected=200):
    if resp.status_code == expected:
        print(f"✅ {name}: {resp.status_code}")
        return True
    else:
        print(f"❌ {name}: {resp.status_code} (Expected {expected})")
        print(f"   Response: {resp.text[:500]}")
        return False

def run_tests():
    its = str(int(time.time()))[-8:]
    print(f"Testing with ITS: {its}")

    # 1. Health Check
    resp = requests.get(f"{BASE_URL}/health/")
    check_status("Public Health Check", resp)

    # 2. Member Create (Admin)
    member_data = {
        "its_number": its,
        "name": f"Verification Test {its}",
        "mohalla": "Post-Cleanup Mohalla",
        "email": f"test_{its}@example.com",
        "mobile": "9876543210"
    }
    resp = requests.post(f"{BASE_URL}/vajebaat/members/", json=member_data, headers=HEADERS)
    if not check_status("Member Create (Admin)", resp, 201): return

    # 3. Public Appointment Booking
    apt_data = {
        "its_number": its,
        "name": f"Verification Test {its}",
        "mobile": "9876543210",
        "preferred_date": "2026-03-20",
        "remarks": "Final Post-Cleanup Audit"
    }
    resp = requests.post(f"{BASE_URL}/vajebaat/appointments/", json=apt_data)
    if not check_status("Public Appointment Booking", resp, 201): return
    apt_id = resp.json()['id']

    # 4. List Dates & Slots (Admin)
    resp = requests.get(f"{BASE_URL}/vajebaat/dates/", headers=HEADERS)
    if not check_status("Dates List (Admin)", resp): return
    dates = resp.json()
    if not dates:
        print("⚠️ No dates available for testing")
        return
    date_id = dates[0]['id']

    resp = requests.get(f"{BASE_URL}/vajebaat/slots/?date_id={date_id}", headers=HEADERS)
    if not check_status("Slots List (Admin)", resp): return
    slots = resp.json()
    if not slots:
        print("⚠️ No slots found for date")
        return
    slot_id = slots[0]['id']

    # 5. Assign Slot (Admin)
    resp = requests.post(f"{BASE_URL}/vajebaat/appointments/{apt_id}/assign-slot/", json={"slot_id": slot_id}, headers=HEADERS)
    check_status("Slot Assignment (Admin)", resp, 200)

    # 6. Reschedule (Admin) - find another slot if exists
    if len(slots) > 1:
        new_slot_id = slots[1]['id']
        resp = requests.patch(f"{BASE_URL}/vajebaat/appointments/{apt_id}/reschedule/", json={"slot_id": new_slot_id}, headers=HEADERS)
        check_status("Reschedule (Admin)", resp, 200)

    # 7. Cancellation (Admin)
    resp = requests.patch(f"{BASE_URL}/vajebaat/appointments/{apt_id}/cancel/", headers=HEADERS)
    check_status("Cancellation (Admin)", resp, 200)

    # 8. CSV Export
    resp = requests.get(f"{BASE_URL}/vajebaat/export-csv/", headers=HEADERS)
    if check_status("CSV Export (Admin)", resp):
        if "ITS,Name,Mobile" in resp.text:
            print("✅ CSV Header Verified")

    # 9. Directory & Stats
    resp = requests.get(f"{BASE_URL}/vajebaat/members-directory/", headers=HEADERS)
    check_status("Members Directory (Admin)", resp)

    resp = requests.get(f"{BASE_URL}/vajebaat/dashboard-stats/", headers=HEADERS)
    check_status("Dashboard Stats (Admin)", resp)

    # 10. Conflict Test: Duplicate Appointment for same ITS should be ALLOWED per current logic (multiple takhmeen possible)
    # But let's check validation on Member ITS
    resp = requests.post(f"{BASE_URL}/vajebaat/members/", json=member_data, headers=HEADERS)
    check_status("Duplicate Member ITS Check (Expect 400)", resp, 400)

    print("\n🚀 API Verification Complete.")

if __name__ == "__main__":
    run_tests()
