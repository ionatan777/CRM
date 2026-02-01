from app.db.session import SessionLocal
from app.models.tenant import Tenant
from app.models.contact import Contact
from app.models.conversation import Conversation
from app.models.message import Message

db = SessionLocal()
print("--- TENANTS ---")
for t in db.query(Tenant).all():
    print(f"ID: {t.id} | Name: {t.name}")

print("\n--- CONTACTS ---")
for c in db.query(Contact).all():
    print(f"ID: {c.id} | Name: {c.name} | Phone: {c.phone} | Tenant: {c.tenant_id}")

db.close()
