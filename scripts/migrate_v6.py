from app.db.session import engine, Base
from app.models.backup import BackupJob
# Ensure other models are loaded if needed for foreign keys, though ForeignKey("tenants.id") usually matches table name
from app.models.tenant import Tenant

def migrate():
    print("Creating new tables for Backups...")
    Base.metadata.create_all(bind=engine)
    print("Migration successful.")

if __name__ == "__main__":
    migrate()
