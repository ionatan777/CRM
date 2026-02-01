import sys
import os
sys.path.append(os.getcwd())

from app.db.session import engine
from sqlalchemy import text
import uuid
import datetime
import random

def seed_data():
    conn = engine.connect()
    trans = conn.begin()
    try:
        # 1. Get Admin User
        result = conn.execute(text("SELECT id, tenant_id FROM users WHERE email = 'admin@crm.com'"))
        user = result.fetchone()
        
        if not user:
            print("User admin@crm.com not found. Run create_user_manual.py first.")
            return

        tenant_id = user[1] # accessing by index
        print(f"Seeding data for Tenant: {tenant_id}")

        # 2. Check/Create Tags
        tags_data = [
            {"name": "Lead", "color": "#3B82F6"},
            {"name": "Customer", "color": "#10B981"},
            {"name": "Urgent", "color": "#EF4444"},
            {"name": "VIP", "color": "#8B5CF6"},
        ]
        
        tags_map = {} # name -> id
        
        for tag_info in tags_data:
            # Check exist
            check = conn.execute(
                text("SELECT id FROM tags WHERE name = :name AND tenant_id = :tenant_id"),
                {"name": tag_info["name"], "tenant_id": tenant_id}
            ).fetchone()
            
            if check:
                tags_map[tag_info["name"]] = check[0]
            else:
                new_id = uuid.uuid4()
                conn.execute(
                    text("INSERT INTO tags (id, tenant_id, name, color, created_at) VALUES (:id, :tenant_id, :name, :color, :now)"),
                    {
                        "id": new_id,
                        "tenant_id": tenant_id,
                        "name": tag_info["name"],
                        "color": tag_info["color"],
                        "now": datetime.datetime.now()
                    }
                )
                tags_map[tag_info["name"]] = new_id
        
        print("Tags synced.")

        # 3. Create Contacts
        contacts_data = [
            {"name": "Alice Johnson", "phone": "+1555001"},
            {"name": "Bob Smith", "phone": "+1555002"},
            {"name": "Charlie Brown", "phone": "+1555003"},
            {"name": "Diana Prince", "phone": "+1555004"},
            {"name": "Evan Wright", "phone": "+1555005"},
        ]

        for c_data in contacts_data:
            # Check exist
            check = conn.execute(
                text("SELECT id FROM contacts WHERE phone = :phone AND tenant_id = :tenant_id"),
                {"phone": c_data["phone"], "tenant_id": tenant_id}
            ).fetchone()
            
            contact_id = None
            if check:
                contact_id = check[0]
            else:
                contact_id = uuid.uuid4()
                conn.execute(
                    text("INSERT INTO contacts (id, tenant_id, name, phone, created_at) VALUES (:id, :tenant_id, :name, :phone, :now)"),
                    {
                        "id": contact_id,
                        "tenant_id": tenant_id,
                        "name": c_data["name"],
                        "phone": c_data["phone"],
                        "now": datetime.datetime.now()
                    }
                )
                
                # Tag association (random)
                if random.random() > 0.3:
                    tag_name = random.choice(list(tags_map.keys()))
                    tag_id = tags_map[tag_name]
                    # Check association
                    assoc_check = conn.execute(
                        text("SELECT * FROM contact_tags WHERE contact_id = :cid AND tag_id = :tid"),
                        {"cid": contact_id, "tid": tag_id}
                    ).fetchone()
                    
                    if not assoc_check:
                         conn.execute(
                            text("INSERT INTO contact_tags (contact_id, tag_id) VALUES (:cid, :tid)"),
                            {"cid": contact_id, "tid": tag_id}
                        )

            # 4. Create Conversation
            check_conv = conn.execute(
                text("SELECT id FROM conversations WHERE contact_id = :cid"),
                {"cid": contact_id}
            ).fetchone()
            
            conv_id = None
            if check_conv:
                conv_id = check_conv[0]
            else:
                conv_id = uuid.uuid4()
                conn.execute(
                    text("INSERT INTO conversations (id, tenant_id, contact_id, status, last_message_at, created_at) VALUES (:id, :tid, :cid, 'open', :now, :now)"),
                    {
                        "id": conv_id,
                        "tid": tenant_id,
                        "cid": contact_id,
                        "now": datetime.datetime.now()
                    }
                )
                
                # 5. Add Messages
                msgs = [
                    ("Hello! I'm interested in your product.", "inbound"),
                    ("Hi there! Sure, what would you like to know?", "outbound"),
                    ("Can you send me a price list?", "inbound"),
                    ("Absolutely, sending it now.", "outbound"),
                ]
                
                base_time = datetime.datetime.now() - datetime.timedelta(hours=random.randint(1, 48))
                
                for i, (content, direction) in enumerate(msgs):
                    msg_time = base_time + datetime.timedelta(minutes=i*5)
                    conn.execute(
                        text("INSERT INTO messages (id, conversation_id, content, type, direction, is_read, created_at) VALUES (:id, :cvid, :content, 'text', :dir, :read, :ts)"),
                        {
                            "id": uuid.uuid4(),
                            "cvid": conv_id,
                            "content": content,
                            "dir": direction,
                            "read": True,
                            "ts": msg_time
                        }
                    )
                
                # Update conv time
                conn.execute(
                    text("UPDATE conversations SET last_message_at = :ts WHERE id = :id"),
                    {
                        "ts": base_time + datetime.timedelta(minutes=20),
                        "id": conv_id
                    }
                )

        trans.commit()
        print("Data seeded successfully (Raw SQL)!")
        
    except Exception as e:
        trans.rollback()
        print(f"Error seeding data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    seed_data()
