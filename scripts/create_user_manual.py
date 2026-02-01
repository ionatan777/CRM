import urllib.request
import urllib.error
import json
import uuid

BASE_URL = "http://localhost:8000/api/v1"

def create_user():
    email = "admin@crm.com"
    password = "password123"
    
    print(f"Creating user: {email} / {password}")
    
    payload = {
        "email": email,
        "password": password,
        "full_name": "Admin User",
        "company_name": "My Company"
    }
    
    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", method="POST", data=data, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            print("User created successfully!")
            print(res_body)
    except urllib.error.HTTPError as e:
        if e.code == 400:
            print("User likely already exists (400 Bad Request).")
        else:
            print(f"Failed to create user: {e.code} - {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_user()
