import urllib.request
import json
import sys

BASE = 'http://127.0.0.1:8000'

def post(path, data):
    url = BASE + path
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'),
                                 headers={'Content-Type': 'application/json'})
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


if __name__ == '__main__':
    username = 'testuser'
    email = 'testuser@example.com'
    password = 'Testpass123!'

    print('Registering user...')
    code, resp = post('/api/auth/register/', {'username': username, 'email': email, 'password': password, 'password2': password})
    print('Register response:', code, resp)

    print('\nLogging in...')
    # Try email first, then username
    code, resp = post('/api/auth/login/', {'email': email, 'password': password})
    print('Login with email response:', code, resp)
    if code != 200 or 'access' not in resp:
        code, resp = post('/api/auth/login/', {'username': username, 'password': password})
        print('Login with username response:', code, resp)

    if resp and isinstance(resp, dict) and 'access' in resp:
        access = resp['access']
        auth_header = f'Bearer {access}'
        print('\nAccess token (truncated):', access[:24] + '...')
        print('Authorization header to be sent:', auth_header)
        print('\nFetching profile with access token...')
        code, profile = get('/api/auth/profile/', token=access)
        print('Profile response:', code, profile)
    else:
        print('\nFailed to get access token; cannot fetch profile')
