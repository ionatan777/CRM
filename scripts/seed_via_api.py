import requests
import random
import datetime
import sys

BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "admin@crm.com"
PASSWORD = "password123"

def get_token():
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data={"username": EMAIL, "password": PASSWORD})
        response.raise_for_status()
        return response.json()["access_token"]
    except Exception as e:
        print(f"Login failed: {e}")
        # Try registering if login fails
        try:
            print("Trying to register user...")
            requests.post(f"{BASE_URL}/auth/register", json={
                "email": EMAIL,
                "password": PASSWORD,
                "full_name": "Administrador",
                "company_name": "Mi Startup"
            })
            # Login again
            response = requests.post(f"{BASE_URL}/auth/login", data={"username": EMAIL, "password": PASSWORD})
            return response.json()["access_token"]
        except:
            print("Could not login or register.")
            sys.exit(1)

def seed():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Logged in as {EMAIL}")

    # 1. Tags (Etiquetas de Negocio)
    tags = [
        {"name": "Interesado", "color": "#3B82F6"},
        {"name": "Cliente VIP", "color": "#10B981"},
        {"name": "Cotización", "color": "#F59E0B"},
        {"name": "Soporte", "color": "#EF4444"},
    ]
    
    created_tags = {}
    print("Creating Tags...")
    
    # We don't have a direct "create tag" endpoint for global tags usually, 
    # but tags are created on the fly or via contact. 
    # Let's create dummy contacts to init tags or valid logic.
    # Actually, the contacts endpoint might not expose independent tag creation easily 
    # depending on implementation. Let's check `contacts.py`.
    # Based on previous read, `add_tag` is /contacts/{id}/tags.
    
    # 2. Contacts (Clientes)
    contacts_data = [
        {"name": "María García", "phone": "+525512340001"},
        {"name": "Juan Pérez", "phone": "+525512340002"},
        {"name": "Empresa Tech SA", "phone": "+525512340003"},
        {"name": "Luisa Martínez", "phone": "+525512340004"},
        {"name": "Carlos López", "phone": "+525512340005"},
    ]

    print("Creating Contacts...")
    for c in contacts_data:
        try:
            # Create Contact
            res = requests.post(f"{BASE_URL}/contacts/", json=c, headers=headers)
            if res.status_code == 200:
                contact = res.json()
                cid = contact["id"]
                
                # Assign Random Tag
                tag_def = random.choice(tags)
                requests.post(f"{BASE_URL}/contacts/{cid}/tags", json=tag_def, headers=headers)
                
                # Add Note
                requests.post(f"{BASE_URL}/contacts/{cid}/notes", json={"content": "Cliente contactado vía campaña de Facebook."}, headers=headers)
                
                # Create Mock Conversation logic via DB (cannot easily do via API if endpoints don't exist specifically for mocking inbound)
                # But wait, we can just use the created contacts to show them in the UI. 
                # To show conversations, we need messages.
                # Assuming we have a way to simulate inbound messages or just send outbound.
                # Let's send an outbound message to initialize conversation.
                
                requests.post(f"{BASE_URL}/messages/", json={"contact_id": cid, "content": "Hola, ¿en qué podemos ayudarte hoy?"}, headers=headers)
                
        except Exception as e:
            print(f"Error creating contact {c['name']}: {e}")

    print("Seeding Complete! Refresh your Dashboard.")

if __name__ == "__main__":
    seed()
