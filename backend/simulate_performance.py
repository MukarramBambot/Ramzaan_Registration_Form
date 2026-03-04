import requests
import time
import random

BASE_URL = "http://localhost:8000/api"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcyNjU2MDU2LCJpYXQiOjE3NzI2NTI0NTYsImp0aSI6IjZjMzZkNjcyZGEzZDRkYjA4NmI0OTIxODhiYTY1MTQ2IiwidXNlcl9pZCI6IjEifQ.rL78f59MYqI0Nbw18N2nUACO3C-XLUYz-lYGKgE-ZgI"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def simulate_load(count=200):
    print(f"🚀 Simulating {count} appointments...")
    start_time = time.time()
    
    # 1. Ensure a date exists
    resp = requests.get(f"{BASE_URL}/vajebaat/dates/", headers=HEADERS)
    dates = resp.json()
    if not dates:
        print("❌ No dates available")
        return
    
    # Use the first active date
    date_obj = next((d for d in dates if d['is_active']), dates[0])
    
    for i in range(count):
        its = f"9000{i:04d}"
        payload = {
            "its_number": its,
            "name": f"Performance Test {i}",
            "mobile": f"987654{i:04d}",
            "preferred_date": date_obj['date'],
            "remarks": "Load Simulation"
        }
        # Batch insert would be better but we test the API endpoint throughput
        resp = requests.post(f"{BASE_URL}/vajebaat/appointments/", json=payload)
        if resp.status_code != 201:
            print(f"❌ Failed at {i}: {resp.status_code}")
            break
        if i % 10 == 0:
            print(f"Progress: {i}/{count}")

    duration = time.time() - start_time
    print(f"✅ Simulation complete in {duration:.2f} seconds.")
    print(f"Avg: {duration/count:.2f}s per request")

if __name__ == "__main__":
    simulate_load(200)
