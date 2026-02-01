from app.db.session import engine, Base
from app.models.audit import AuditLog

def migrate():
    print("Creating new tables for Audit Logs...")
    Base.metadata.create_all(bind=engine)
    print("Migration successful.")

if __name__ == "__main__":
    migrate()
