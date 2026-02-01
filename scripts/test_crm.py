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
            return json.loads(res_body) if res_body else None
    except Exception as e:
        print(f"Error [{method} {url}]: {e}")
        return None

def test_crm_flow():
    print("\n--- 1. Get List of Contacts ---")
    contacts = make_request(f"{BASE_URL}/contacts/?tenant_id={TENANT_ID}")
    if not contacts:
        print("No contacts found. Run previous tests first.")
        return
    
    contact_id = contacts[0]['id']
    print(f"Testing with Contact: {contacts[0]['name']} ({contact_id})")

    print("\n--- 2. Add Tag 'VIP' ---")
    tag_payload = {"name": "VIP", "color": "#FFC107"}
    tag_res = make_request(f"{BASE_URL}/contacts/{contact_id}/tags?tenant_id={TENANT_ID}", "POST", tag_payload)
    print(f"Tag Added: {tag_res}")

    print("\n--- 3. Add Note 'Follow up' ---")
    note_payload = {"content": "Customer requested a demo on Friday."}
    note_res = make_request(f"{BASE_URL}/contacts/{contact_id}/notes?tenant_id={TENANT_ID}", "POST", note_payload)
    print(f"Note Added: {note_res}")

    print("\n--- 4. Verify Contact Details ---")
    contact_detail = make_request(f"{BASE_URL}/contacts/{contact_id}?tenant_id={TENANT_ID}")
    
    tags = contact_detail.get('tags', [])
    notes = contact_detail.get('notes', [])
    
    print(f"Tags found: {[t['name'] for t in tags]}")
    print(f"Notes found: {len(notes)}")
    
    if "VIP" in [t['name'] for t in tags] and len(notes) > 0:
        print("SUCCESS: CRM Features Verified")
    else:
        print("FAILURE: Tags or Notes missing")

if __name__ == "__main__":
    test_crm_flow()
