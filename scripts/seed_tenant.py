from app.db.session import SessionLocal
from app.models.tenant import Tenant
import uuid

db = SessionLocal()
try:
    tenant_id = uuid.uuid4()
    tenant = Tenant(id=tenant_id, name="Test Business", slug="test-biz")
    db.add(tenant)
    db.commit()
    print(f"CREATED_TENANT_ID={tenant_id}")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
