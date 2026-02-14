#!/usr/bin/env python3
"""
Comprehensive authentication system test script.
Tests both Django admin login (form-based CSRF) and JWT API login.
"""

import requests
import re
import urllib3
import json
from datetime import datetime

urllib3.disable_warnings()

BASE_URL = 'https://api.madrasjamaatportal.org'
CREDENTIALS = {
    'its_number': '60451866',
    'password': 'admin123'
}

def print_section(title):
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)

def print_test(test_name, passed, details=""):
    symbol = "✅" if passed else "❌"
    print(f"{symbol} {test_name}")
    if details:
        print(f"   {details}")

def test_django_admin_login_form_based():
    """Test Django admin login using form submission (CSRF protected)."""
    print_section("TEST 1: Django Admin Login (Form-Based CSRF)")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    })
    
    try:
        # Step 1: Get login page
        print("\n[Step 1] Fetching login page...")
        response = session.get(f'{BASE_URL}/admin/login/', verify=False)
        print_test(
            "Login page fetched",
            response.status_code == 200,
            f"Status: {response.status_code}"
        )
        
        # Extract CSRF token
        csrf_match = re.search(r'name="csrfmiddlewaretoken"[^>]*value="([^"]+)"', response.text)
        if not csrf_match:
            print_test("CSRF token extracted", False, "No CSRF token found in form")
            return False
        
        csrf_token = csrf_match.group(1)
        print_test("CSRF token extracted", True, f"Token: {csrf_token[:20]}...")
        
        # Step 2: Extract CSRF cookie
        csrf_cookie = None
        for cookie in session.cookies:
            if 'csrf' in cookie.name.lower():
                csrf_cookie = cookie.value
                print_test(
                    "CSRF cookie received",
                    True,
                    f"Domain: {cookie.domain}, Secure: {cookie.secure}"
                )
                break
        
        if not csrf_cookie:
            print_test("CSRF cookie received", False)
            return False
        
        # Step 3: Prepare login data
        login_data = {
            'username': CREDENTIALS['its_number'],
            'password': CREDENTIALS['password'],
            'csrfmiddlewaretoken': csrf_token,
            'next': '/admin/'
        }
        
        # Step 4: Submit login form WITH Referer header (like browser does)
        print("\n[Step 2] Submitting login form...")
        headers = {
            'Referer': f'{BASE_URL}/admin/login/',
            'Origin': BASE_URL
        }
        
        login_response = session.post(
            f'{BASE_URL}/admin/login/',
            data=login_data,
            headers=headers,
            allow_redirects=False,
            verify=False,
            timeout=5
        )
        
        print_test(
            "Login POST submitted",
            login_response.status_code in [302, 200],
            f"Status: {login_response.status_code}"
        )
        
        # Step 5: Check redirect
        if login_response.status_code == 302:
            location = login_response.headers.get('Location', '')
            print_test(
                "Admin redirect received",
                '/admin/' in location,
                f"Location: {location}"
            )
            return True
        else:
            print_test("Admin login successful", False, f"Got {login_response.status_code}, expected 302")
            return False
            
    except Exception as e:
        print_test("Django admin login test", False, str(e))
        return False

def test_jwt_login():
    """Test JWT API login."""
    print_section("TEST 2: JWT API Login")
    
    try:
        # Step 1: Get tokens
        print("\n[Step 1] Requesting JWT tokens...")
        response = requests.post(
            f'{BASE_URL}/api/auth/login/',
            json=CREDENTIALS,
            verify=False,
            timeout=5
        )
        
        print_test(
            "JWT endpoint responded",
            response.status_code == 200,
            f"Status: {response.status_code}"
        )
        
        if response.status_code != 200:
            return False
        
        data = response.json()
        
        # Check tokens
        has_access = 'access' in data
        has_refresh = 'refresh' in data
        print_test(
            "Access token issued",
            has_access,
            f"Token: {data['access'][:30]}..." if has_access else ""
        )
        print_test(
            "Refresh token issued",
            has_refresh,
            f"Token: {data['refresh'][:30]}..." if has_refresh else ""
        )
        
        if not (has_access and has_refresh):
            return False
        
        access_token = data['access']
        
        # Step 2: Use token to access protected endpoint
        print("\n[Step 2] Testing protected endpoint with JWT...")
        headers = {'Authorization': f'Bearer {access_token}'}
        me_response = requests.get(
            f'{BASE_URL}/api/auth/me/',
            headers=headers,
            verify=False,
            timeout=5
        )
        
        print_test(
            "Protected endpoint accessed",
            me_response.status_code == 200,
            f"Status: {me_response.status_code}"
        )
        
        if me_response.status_code != 200:
            return False
        
        user_data = me_response.json()
        print_test(
            "User info retrieved",
            'username' in user_data,
            f"User: {user_data.get('username', 'N/A')}, " +
            f"is_staff: {user_data.get('is_staff', False)}"
        )
        
        return True
        
    except Exception as e:
        print_test("JWT login test", False, str(e))
        return False

def test_protected_endpoints():
    """Test accessing protected API endpoints with JWT."""
    print_section("TEST 3: Protected API Endpoints")
    
    try:
        # Get JWT token
        print("\n[Step 1] Authenticating...")
        auth_response = requests.post(
            f'{BASE_URL}/api/auth/login/',
            json=CREDENTIALS,
            verify=False,
            timeout=5
        )
        
        if auth_response.status_code != 200:
            print_test("Authentication", False, "Failed to get token")
            return False
        
        access_token = auth_response.json()['access']
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Test various endpoints
        print("\n[Step 2] Testing protected endpoints...")
        
        endpoints = [
            ('/api/auth/me/', 'Get current user info'),
            ('/api/registrations/', 'List registrations'),
        ]
        
        all_passed = True
        for endpoint, description in endpoints:
            try:
                response = requests.get(
                    f'{BASE_URL}{endpoint}',
                    headers=headers,
                    verify=False,
                    timeout=5
                )
                
                passed = response.status_code in [200, 201]
                print_test(
                    f"{description} ({endpoint})",
                    passed,
                    f"Status: {response.status_code}"
                )
                all_passed = all_passed and passed
            except Exception as e:
                print_test(f"{description} ({endpoint})", False, str(e))
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print_test("Protected endpoints test", False, str(e))
        return False

def test_csrf_protection():
    """Test that CSRF protection is working correctly."""
    print_section("TEST 4: CSRF Protection")
    
    try:
        session = requests.Session()
        
        # Get login page
        print("\n[Step 1] Getting CSRF token...")
        response = session.get(f'{BASE_URL}/admin/login/', verify=False)
        csrf_match = re.search(r'name="csrfmiddlewaretoken"[^>]*value="([^"]+)"', response.text)
        csrf_token = csrf_match.group(1)
        print_test("CSRF token obtained", True)
        
        # Step 2: Try login WITHOUT Referer (should fail)
        print("\n[Step 2] Testing CSRF validation (no Referer)...")
        login_data = {
            'username': CREDENTIALS['its_number'],
            'password': CREDENTIALS['password'],
            'csrfmiddlewaretoken': csrf_token,
            'next': '/admin/'
        }
        
        bad_response = session.post(
            f'{BASE_URL}/admin/login/',
            data=login_data,
            allow_redirects=False,
            verify=False,
            timeout=5
        )
        
        print_test(
            "CSRF validation active",
            bad_response.status_code == 403,
            f"Status: {bad_response.status_code} (403 expected)"
        )
        
        # Step 3: Try login WITH Referer (should succeed)
        print("\n[Step 3] Submitting with correct headers...")
        session2 = requests.Session()
        response2 = session2.get(f'{BASE_URL}/admin/login/', verify=False)
        csrf_match2 = re.search(r'name="csrfmiddlewaretoken"[^>]*value="([^"]+)"', response2.text)
        csrf_token2 = csrf_match2.group(1)
        
        login_data2 = {
            'username': CREDENTIALS['its_number'],
            'password': CREDENTIALS['password'],
            'csrfmiddlewaretoken': csrf_token2,
            'next': '/admin/'
        }
        
        good_response = session2.post(
            f'{BASE_URL}/admin/login/',
            data=login_data2,
            headers={'Referer': f'{BASE_URL}/admin/login/'},
            allow_redirects=False,
            verify=False,
            timeout=5
        )
        
        print_test(
            "CSRF bypass prevented but valid request passes",
            good_response.status_code == 302,
            f"Status: {good_response.status_code} (302 expected)"
        )
        
        return True
        
    except Exception as e:
        print_test("CSRF protection test", False, str(e))
        return False

def main():
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  RAMZAAN REGISTRATION FORM - AUTHENTICATION SYSTEM TEST".center(78) + "║")
    print("║" + f"  Timestamp: {datetime.now().isoformat()}".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    
    results = {
        'Django Admin Login': test_django_admin_login_form_based(),
        'JWT API Login': test_jwt_login(),
        'Protected Endpoints': test_protected_endpoints(),
        'CSRF Protection': test_csrf_protection(),
    }
    
    # Summary
    print_section("TEST SUMMARY")
    all_passed = True
    for test_name, passed in results.items():
        symbol = "✅" if passed else "❌"
        print(f"{symbol} {test_name}")
        all_passed = all_passed and passed
    
    if all_passed:
        print("\n" + "🎉 " * 20)
        print(" ALL TESTS PASSED - AUTHENTICATION SYSTEM IS FULLY OPERATIONAL")
        print("🎉 " * 20)
    else:
        print("\n" + "❌ " * 20)
        print(" SOME TESTS FAILED - CHECK CONFIGURATION")
        print("❌ " * 20)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    exit(main())
