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

def test_inbox_flow():
    print("\n--- 1. List Conversations (Initial) ---")
    convs = make_request(f"{BASE_URL}/conversations/?tenant_id={TENANT_ID}")
    print(f"Conversations found: {len(convs) if convs else 0}")
    if convs:
        print(f"Top Conv: {convs[0]['contact']['name']} | Unread: {convs[0]['unread_count']}")
        conv_id = convs[0]['id']

        print(f"\n--- 2. List Messages for Conv {conv_id} ---")
        msgs = make_request(f"{BASE_URL}/conversations/{conv_id}/messages?tenant_id={TENANT_ID}")
        print(f"Messages found: {len(msgs) if msgs else 0}")
        if msgs:
            print(f"First Msg: {msgs[0]['content']} | Read: {msgs[0]['is_read']}")

        print(f"\n--- 3. Mark as Read ---")
        res = make_request(f"{BASE_URL}/conversations/{conv_id}/read?tenant_id={TENANT_ID}", "POST")
        print(f"Mark Read Result: {res}")

        print("\n--- 4. List Conversations (After Read) ---")
        convs_after = make_request(f"{BASE_URL}/conversations/?tenant_id={TENANT_ID}")
        if convs_after:
             print(f"Top Conv Unread: {convs_after[0]['unread_count']}")

if __name__ == "__main__":
    test_inbox_flow()
