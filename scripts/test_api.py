import urllib.request
import json
import urllib.error

BASE_URL = "http://localhost:8000/api/v1"
TENANT_ID = "47f6ef09-db11-9344-b4e8-5eef09db1193"

def make_request(url, method="GET", data=None):
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(url, method=method, headers=headers)
    if data:
        req.data = json.dumps(data).encode('utf-8')
    
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            print(f"{method} {url} Status: {response.status}")
            print("Response:", res_body)
            return json.loads(res_body)
    except urllib.error.HTTPError as e:
        print(f"Error {e.code}: {e.read().decode()}")
    except Exception as e:
        print(f"Error: {e}")

def test_create_contact():
    print(f"Testing Create Contact for Tenant: {TENANT_ID}")
    url = f"{BASE_URL}/contacts/?tenant_id={TENANT_ID}"
    payload = {
        "phone": "555123456",
        "name": "Juan Perez",
        "metadata": {"source": "script"}
    }
    make_request(url, "POST", payload)

def test_list_contacts():
    print("Testing List Contacts...")
    url = f"{BASE_URL}/contacts/?tenant_id={TENANT_ID}"
    make_request(url, "GET")

if __name__ == "__main__":
    test_create_contact()
    test_list_contacts()
