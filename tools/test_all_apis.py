"""
Comprehensive API test script for KnowledgeHub
Tests all authentication endpoints and verifies they work correctly.
"""
import urllib.request
import json
import sys
import time

BASE = 'http://127.0.0.1:8000'

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.RESET}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.RESET}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.RESET}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.RESET}")

def post(path, data, token=None):
    """Make a POST request"""
    url = BASE + path
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.getcode(), json.load(resp)
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode('utf-8')
            return e.code, json.loads(body)
        except Exception:
            return e.code, {'error': str(e)}
    except Exception as e:
        return None, {'error': str(e)}

def get(path, token=None):
    """Make a GET request"""
    url = BASE + path
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.getcode(), json.load(resp)
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode('utf-8')
            return e.code, json.loads(body)
        except Exception:
            return e.code, {'error': str(e)}
    except Exception as e:
        return None, {'error': str(e)}

def put(path, data, token=None):
    """Make a PUT request"""
    url = BASE + path
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='PUT')
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.getcode(), json.load(resp)
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode('utf-8')
            return e.code, json.loads(body)
        except Exception:
            return e.code, {'error': str(e)}
    except Exception as e:
        return None, {'error': str(e)}

def test_register():
    """Test user registration"""
    print_info("\n=== Testing Registration ===")
    
    # Test 1: Valid registration
    username = f'testuser_{int(time.time())}'
    email = f'testuser_{int(time.time())}@example.com'
    password = 'Testpass123!'
    
    print(f"Registering user: {username}")
    code, resp = post('/api/auth/register/', {
        'username': username,
        'email': email,
        'password': password,
        'password2': password,
        'full_name': 'Test User'
    })
    
    if code == 201:
        print_success(f"Registration successful: {code}")
        return username, email, password, resp
    else:
        print_error(f"Registration failed: {code} - {resp}")
        return None, None, None, None

def test_register_validation():
    """Test registration validation"""
    print_info("\n=== Testing Registration Validation ===")
    
    # Test password mismatch
    print("Testing password mismatch...")
    code, resp = post('/api/auth/register/', {
        'username': 'testuser2',
        'email': 'test2@example.com',
        'password': 'Testpass123!',
        'password2': 'DifferentPass123!'
    })
    if code == 400:
        print_success(f"Password mismatch validation works: {code}")
    else:
        print_error(f"Password mismatch validation failed: {code} - {resp}")
    
    # Test duplicate email
    print("Testing duplicate email...")
    code, resp = post('/api/auth/register/', {
        'username': 'testuser3',
        'email': 'duplicate@example.com',
        'password': 'Testpass123!',
        'password2': 'Testpass123!'
    })
    if code == 201:
        # Try to register again with same email
        code2, resp2 = post('/api/auth/register/', {
            'username': 'testuser4',
            'email': 'duplicate@example.com',
            'password': 'Testpass123!',
            'password2': 'Testpass123!'
        })
        if code2 == 400:
            print_success(f"Duplicate email validation works: {code2}")
        else:
            print_warning(f"Duplicate email validation may not be working: {code2} - {resp2}")

def test_login(username, email, password):
    """Test login with username and email"""
    print_info("\n=== Testing Login ===")
    
    # Test login with email
    print(f"Logging in with email: {email}")
    code, resp = post('/api/auth/login/', {'email': email, 'password': password})
    
    if code == 200 and 'access' in resp and 'refresh' in resp:
        print_success(f"Login with email successful: {code}")
        return resp['access'], resp['refresh']
    
    # Try with username
    print(f"Logging in with username: {username}")
    code, resp = post('/api/auth/login/', {'username': username, 'password': password})
    
    if code == 200 and 'access' in resp and 'refresh' in resp:
        print_success(f"Login with username successful: {code}")
        return resp['access'], resp['refresh']
    else:
        print_error(f"Login failed: {code} - {resp}")
        return None, None

def test_token_refresh(refresh_token):
    """Test token refresh"""
    print_info("\n=== Testing Token Refresh ===")
    
    code, resp = post('/api/auth/token/refresh/', {'refresh': refresh_token})
    
    if code == 200 and 'access' in resp:
        print_success(f"Token refresh successful: {code}")
        return resp['access']
    else:
        print_error(f"Token refresh failed: {code} - {resp}")
        return None

def test_token_verify(access_token):
    """Test token verification"""
    print_info("\n=== Testing Token Verify ===")
    
    code, resp = post('/api/auth/token/verify/', {'token': access_token})
    
    if code == 200:
        print_success(f"Token verification successful: {code}")
        return True
    else:
        print_error(f"Token verification failed: {code} - {resp}")
        return False

def test_profile_get(access_token):
    """Test getting user profile"""
    print_info("\n=== Testing Get Profile ===")
    
    code, resp = get('/api/auth/profile/', token=access_token)
    
    if code == 200:
        print_success(f"Get profile successful: {code}")
        print(f"  User data: {json.dumps(resp, indent=2)}")
        return resp
    else:
        print_error(f"Get profile failed: {code} - {resp}")
        return None

def test_profile_update(access_token):
    """Test updating user profile"""
    print_info("\n=== Testing Update Profile ===")
    
    update_data = {
        'full_name': 'Updated Test User',
        'avatar_url': 'https://example.com/avatar.jpg'
    }
    
    code, resp = put('/api/auth/profile/', update_data, token=access_token)
    
    if code == 200:
        print_success(f"Update profile successful: {code}")
        print(f"  Updated data: {json.dumps(resp, indent=2)}")
        return resp
    else:
        print_error(f"Update profile failed: {code} - {resp}")
        return None

def test_profile_unauthorized():
    """Test profile access without token"""
    print_info("\n=== Testing Profile Without Token ===")
    
    code, resp = get('/api/auth/profile/')
    
    if code == 401:
        print_success(f"Unauthorized access correctly blocked: {code}")
        return True
    else:
        print_error(f"Unauthorized access not blocked: {code} - {resp}")
        return False

def test_logout(refresh_token, access_token):
    """Test logout"""
    print_info("\n=== Testing Logout ===")
    
    # Test logout without refresh token
    print("Testing logout without refresh token...")
    code, resp = post('/api/auth/logout/', {}, token=access_token)
    if code == 400:
        print_success(f"Logout validation works (no refresh token): {code}")
    else:
        print_warning(f"Logout without refresh token: {code} - {resp}")
    
    # Test logout with refresh token
    print("Testing logout with refresh token...")
    code, resp = post('/api/auth/logout/', {'refresh': refresh_token}, token=access_token)
    
    if code == 200:
        print_success(f"Logout successful: {code}")
        
        # Verify token is blacklisted by trying to refresh it
        print("Verifying token is blacklisted...")
        code2, resp2 = post('/api/auth/token/refresh/', {'refresh': refresh_token})
        if code2 == 401:
            print_success("Token successfully blacklisted (cannot refresh)")
        else:
            print_warning(f"Token may not be blacklisted: {code2} - {resp2}")
        
        return True
    else:
        print_error(f"Logout failed: {code} - {resp}")
        return False

def main():
    print_info("=" * 60)
    print_info("KnowledgeHub API Test Suite")
    print_info("=" * 60)
    
    # Check if server is running
    try:
        code, _ = get('/api/auth/register/')
        if code is None:
            print_error("Cannot connect to server. Make sure Django server is running on http://127.0.0.1:8000")
            sys.exit(1)
        print_info("Server connection successful!")
    except Exception as e:
        print_error(f"Cannot connect to server: {e}")
        print_info("Please start the Django server with: python manage.py runserver")
        sys.exit(1)
    
    # Run tests
    results = {
        'register': False,
        'login': False,
        'token_refresh': False,
        'token_verify': False,
        'profile_get': False,
        'profile_update': False,
        'profile_unauthorized': False,
        'logout': False
    }
    
    # Test registration
    username, email, password, register_resp = test_register()
    if username:
        results['register'] = True
        test_register_validation()
    
    # Test login
    access_token, refresh_token = test_login(username, email, password)
    if access_token:
        results['login'] = True
        
        # Test token operations
        new_access_token = test_token_refresh(refresh_token)
        if new_access_token:
            results['token_refresh'] = True
            access_token = new_access_token  # Use refreshed token
        
        if test_token_verify(access_token):
            results['token_verify'] = True
        
        # Test profile
        if test_profile_get(access_token):
            results['profile_get'] = True
        
        if test_profile_update(access_token):
            results['profile_update'] = True
        
        if test_profile_unauthorized():
            results['profile_unauthorized'] = True
        
        # Test logout
        if test_logout(refresh_token, access_token):
            results['logout'] = True
    
    # Summary
    print_info("\n" + "=" * 60)
    print_info("Test Summary")
    print_info("=" * 60)
    
    for test_name, passed in results.items():
        if passed:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    total = len(results)
    passed = sum(results.values())
    print_info(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("\n🎉 All tests passed! APIs are working correctly.")
        return 0
    else:
        print_error(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

