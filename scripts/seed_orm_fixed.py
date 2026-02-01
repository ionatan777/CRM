import sys
import os
sys.path.append(os.getcwd())

from app.db.session import SessionLocal

# STRICT IMPORT ORDER to satisfy SQLAlchemy mappers
from app.models.tenant import Tenant
from app.models.user import User
from app.models.tag import Tag
from app.models.contact import Contact
from app.models.conversation import Conversation, ConversationStatus
from app.models.message import Message, MessageDirection, MessageType

from sqlalchemy.orm import configure_mappers
configure_mappers()

import datetime
import random

def seed_data():
    db = SessionLocal()
    try:
        # 1. Get Admin User
        user = db.query(User).filter(User.email == "admin@crm.com").first()
        if not user:
            print("User admin@crm.com not found.")
            return

        tenant_id = user.tenant_id
        print(f"Seeding data for Tenant: {tenant_id}")

        # 2. Create Tags
        tags_data = [
            {"name": "Lead", "color": "#3B82F6"},
            {"name": "Customer", "color": "#10B981"},
            {"name": "Urgent", "color": "#EF4444"},
            {"name": "VIP", "color": "#8B5CF6"},
        ]
        
        tags_map = {}
        for tag_info in tags_data:
            tag = db.query(Tag).filter(Tag.name == tag_info["name"], Tag.tenant_id == tenant_id).first()
            if not tag:
                tag = Tag(name=tag_info["name"], color=tag_info["color"], tenant_id=tenant_id)
                db.add(tag)
            tags_map[tag_info["name"]] = tag
        
        db.commit()
        print("Tags created.")

        # 3. Create Contacts
        contacts_data = [
            {"name": "Alice Johnson", "phone": "+1555001"},
            {"name": "Bob Smith", "phone": "+1555002"},
            {"name": "Charlie Brown", "phone": "+1555003"},
            {"name": "Diana Prince", "phone": "+1555004"},
            {"name": "Evan Wright", "phone": "+1555005"},
        ]

        for c_data in contacts_data:
            contact = db.query(Contact).filter(Contact.phone == c_data["phone"], Contact.tenant_id == tenant_id).first()
            if not contact:
                contact = Contact(name=c_data["name"], phone=c_data["phone"], tenant_id=tenant_id)
                db.add(contact)
                db.commit()
                db.refresh(contact)
                
                # Add random tag
                if random.random() > 0.3:
                    tag_name = random.choice(list(tags_map.keys()))
                    # Re-query tag to ensure it's attached to this session if needed (though tags_map holds objects)
                    # Safe to just append if object is valid
                    if tags_map[tag_name] not in contact.tags:
                       contact.tags.append(tags_map[tag_name])
                       db.commit()

            # 4. Create Conversation
            conv = db.query(Conversation).filter(Conversation.contact_id == contact.id).first()
            if not conv:
                conv = Conversation(contact_id=contact.id, tenant_id=tenant_id, status=ConversationStatus.OPEN)
                db.add(conv)
                db.commit()
                db.refresh(conv)

                # 5. Add Messages
                msgs = [
                    ("Hello! I'm interested in your product.", MessageDirection.INBOUND),
                    ("Hi there! Sure, what would you like to know?", MessageDirection.OUTBOUND),
                    ("Can you send me a price list?", MessageDirection.INBOUND),
                    ("Absolutely, sending it now.", MessageDirection.OUTBOUND),
                ]
                
                base_time = datetime.datetime.now() - datetime.timedelta(hours=random.randint(1, 48))

                for i, (content, direction) in enumerate(msgs):
                    msg = Message(
                        conversation_id=conv.id,
                        content=content,
                        direction=direction,
                        is_read=True if direction == MessageDirection.OUTBOUND else False,
                        created_at=base_time + datetime.timedelta(minutes=i*2)
                    )
                    db.add(msg)
                
                conv.last_message_at = base_time + datetime.timedelta(minutes=10)
                db.commit()

        print("Data seeded successfully!")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
