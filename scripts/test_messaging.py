import urllib.request
import json
import uuid

BASE_URL = "http://localhost:8000/api/v1"
TENANT_ID = "47f61e5d-0d94-4961-b4e8-5ef09db11934"

def make_request(url, method="GET", data=None):
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(url, method=method, headers=headers)
    if data:
        req.data = json.dumps(data).encode('utf-8')
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            print(f"[{method}] {url} -> {response.status}")
            return json.loads(res_body) if res_body else None
    except Exception as e:
        print(f"Error: {e}")
        return None

def simulate_verification():
    print("\n--- Simulating Webhook Verification ---")
    url = f"{BASE_URL}/webhooks/whatsapp?hub.mode=subscribe&hub.verify_token=my_secure_verify_token&hub.challenge=123"
    try:
        with urllib.request.urlopen(url) as response:
            print(f"Challenge Response: {response.read().decode('utf-8')}")
    except Exception as e:
        print(f"Verification Failed: {e}")

def simulate_incoming_message():
    print("\n--- Simulating Incoming Webhook ---")
    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {
                        "display_phone_number": "16505551111",
                        "phone_number_id": "123456123"
                    },
                    "contacts": [{
                        "profile": {"name": "Test User"},
                        "wa_id": "16315551181"
                    }],
                    "messages": [{
                        "from": "16315551181",
                        "id": "wamid.HBgL...",
                        "timestamp": "1673887076",
                        "text": {"body": "Hello Jarvis!"},
                        "type": "text"
                    }]
                },
                "field": "messages"
            }]
        }]
    }
    res = make_request(f"{BASE_URL}/webhooks/whatsapp", "POST", payload)
    print("Webhook Result:", res)

def simulate_outbound_message():
    print("\n--- Simulating Outbound Message ---")
    # First get contact created by incoming simulation
    contacts = make_request(f"{BASE_URL}/contacts/?tenant_id={TENANT_ID}", "GET")
    print("Contacts Found:", contacts) # Debug line
    if not contacts:
        print("No contacts found. Run incoming simulation first.")
        return

    contact_id = contacts[0]['id']
    payload = {
        "contact_id": contact_id,
        "content": "Hello from Jarvis Agent!"
    }
    
    res = make_request(f"{BASE_URL}/messages/?tenant_id={TENANT_ID}", "POST", payload)
    print("Outbound Result:", res)

if __name__ == "__main__":
    simulate_verification()
    simulate_incoming_message()
    simulate_outbound_message()
