import urllib.request
import json
import uuid
import time

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
            try:
                return json.loads(res_body)
            except:
                return res_body
    except Exception as e:
        print(f"Error [{method} {url}]: {e}")
        return None

def test_backup_flow():
    print("\n--- 1. Trigger Backup ---")
    res = make_request(f"{BASE_URL}/backups/?tenant_id={TENANT_ID}", "POST")
    print(f"Trigger Result: {res}")
    
    if not res or 'job_id' not in res:
        print("Failed to trigger backup")
        return

    job_id = res['job_id']
    
    print("\n--- 2. Poll Status ---")
    for _ in range(5):
        status_res = make_request(f"{BASE_URL}/backups/{job_id}?tenant_id={TENANT_ID}")
        print(f"Status: {status_res}")
        
        # If it returns a file content (dict or list), it's done. 
        # But wait, our API returns FileResponse, which urllib reads as bytes -> string.
        # If it's a JSON string, it might be the content.
        # Status endpoint returns {"status": "pending"} if not ready.
        
        if isinstance(status_res, dict) and 'status' in status_res:
            if status_res['status'] == 'pending':
                time.sleep(1)
                continue
            if status_res['status'] == 'failed':
                print("Backup Failed")
                break
        
        # If we got here, we likely got the file content
        print("Backup Completed! File content received.")
        if isinstance(status_res, dict) and 'contacts' in status_res:
            print(f"Contacts in backup: {len(status_res['contacts'])}")
        break

if __name__ == "__main__":
    test_backup_flow()
