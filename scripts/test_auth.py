import urllib.request
import urllib.error
import json

BASE_URL = "http://localhost:8000/api/v1"

def make_request(url, method="GET", data=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    req = urllib.request.Request(url, method=method, headers=headers)
    
    # Handle form-urlencoded for OAuth2 login if needed, but our endpoint accepts JSON?
    # Wait, OAuth2PasswordRequestForm expects form data.
    if method == "POST" and "auth/login" in url:
        # Special case for Login form data
        data_encoded = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(url, method=method, data=data_encoded) # default content-type is form-urlencoded
    elif data:
        req.data = json.dumps(data).encode('utf-8')

    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            return json.loads(res_body) if res_body else None
    except urllib.error.HTTPError as e:
        print(f"HTTP Error [{method} {url}]: {e.code} - {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"Error [{method} {url}]: {e}")
        return None

def test_auth_flow():
    email = f"admin_{uuid.uuid4()}@example.com"
    password = "secret_password"
    
    print(f"\n--- 1. Register User ({email}) ---")
    reg_payload = {
        "email": email,
        "password": password,
        "full_name": "Admin User",
        "company_name": f"Secure Corp {uuid.uuid4()}"
    }
    reg_res = make_request(f"{BASE_URL}/auth/register", "POST", reg_payload)
    print(f"Register Result: {reg_res}")
    
    if not reg_res or 'access_token' not in reg_res:
        print("Registration Failed")
        return

    # 2. Login (Verification)
    print("\n--- 2. Login ---")
    login_payload = {"username": email, "password": password}
    login_res = make_request(f"{BASE_URL}/auth/login", "POST", login_payload)
    print(f"Login Result: {login_res}")
    
    token = login_res['access_token']

    # 3. Access Protected Route
    print("\n--- 3. Access Protected Route (Create Contact) ---")
    contact_payload = {"name": "Secure Client", "phone": "555000999"}
    contact_res = make_request(f"{BASE_URL}/contacts/", "POST", contact_payload, token=token)
    print(f"Create Contact Result: {contact_res}")
    
    if contact_res and contact_res.get('name') == "Secure Client":
        print("SUCCESS: Auth Flow Verified")
    else:
        print("FAILURE: Could not access protected route")

    # 4. Access Without Token (Should Fail)
    print("\n--- 4. Access Without Token (Expect 401) ---")
    fail_res = make_request(f"{BASE_URL}/contacts/", "POST", contact_payload)
    if not fail_res: 
        print("SUCCESS: Rejected unauthorized request")


import uuid
if __name__ == "__main__":
    test_auth_flow()
