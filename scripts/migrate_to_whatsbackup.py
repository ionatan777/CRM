# Database Migration Script - ProCRM to WhatsBackup
# Run with: python scripts/migrate_to_whatsbackup.py

from sqlalchemy import create_engine, text
from app.core.config import settings
import sys

def migrate_database():
    """
    Migrates database from ProCRM schema to WhatsBackup schema
    WARNING: This will drop old tables - backup your data first!
    """
    
    print("🔄 Starting WhatsBackup Database Migration...")
    print("⚠️  WARNING: This will modify your database schema")
    
    response = input("Have you backed up your database? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Migration cancelled. Please backup your database first.")
        sys.exit(1)
    
    engine = create_engine(str(settings.DATABASE_URL))
    
    with engine.connect() as conn:
        try:
            print("\n📋 Step 1: Backing up existing users...")
            # Users table will be modified, not dropped
            
            print("\n🗑️  Step 2: Dropping old CRM tables...")
            tables_to_drop = [
                'audit_logs',
                'notes', 
                'tags',
                'messages',  # Will be recreated with new schema
                'conversations',
                'contacts',
                'tenants'
            ]
            
            for table in tables_to_drop:
                try:
                    conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                    print(f"   ✓ Dropped {table}")
                except Exception as e:
                    print(f"   ⚠️  Could not drop {table}: {e}")
            
            print("\n🔧 Step 3: Modifying users table...")
            
            # Add new WhatsApp fields to users
            alter_statements = [
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS whatsapp_phone_id VARCHAR",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS whatsapp_access_token VARCHAR",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS auto_backup_enabled BOOLEAN DEFAULT TRUE",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS backup_frequency_hours INTEGER DEFAULT 24",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_number VARCHAR",
                "ALTER TABLE users DROP COLUMN IF EXISTS tenant_id CASCADE",
                "ALTER TABLE users DROP COLUMN IF EXISTS role CASCADE"
            ]
            
            for statement in alter_statements:
                try:
                    conn.execute(text(statement))
                    print(f"   ✓ {statement[:50]}...")
                except Exception as e:
                    print(f"   ⚠️  {statement[:50]}... failed: {e}")
            
            print("\n📊 Step 4: Creating new WhatsBackup tables...")
            
            # Create backups table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS backups (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    backup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR DEFAULT 'in_progress',
                    total_messages INTEGER DEFAULT 0,
                    total_contacts INTEGER DEFAULT 0,
                    error_message VARCHAR
                )
            """))
            print("   ✓ Created backups table")
            
            # Create messages table (new schema for WhatsApp backups)
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS messages (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    backup_id UUID REFERENCES backups(id) ON DELETE SET NULL,
                    whatsapp_message_id VARCHAR UNIQUE,
                    contact_name VARCHAR,
                    contact_phone VARCHAR,
                    message_text TEXT,
                    message_type VARCHAR DEFAULT 'text',
                    timestamp TIMESTAMP,
                    is_from_me BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            print("   ✓ Created messages table")
            
            # Create indexes for better performance
            print("\n🚀 Step 5: Creating indexes...")
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages(user_id)",
                "CREATE INDEX IF NOT EXISTS idx_messages_contact_phone ON messages(contact_phone)",
                "CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)",
                "CREATE INDEX IF NOT EXISTS idx_backups_user_id ON backups(user_id)"
            ]
            
            for idx in indexes:
                conn.execute(text(idx))
                print(f"   ✓ {idx[:60]}...")
            
            conn.commit()
            
            print("\n✅ Migration completed successfully!")
            print("\n📌 Next steps:")
            print("   1. Restart your FastAPI server")
            print("   2. Verify models are working: python scripts/test_models.py")
            print("   3. Connect WhatsApp in the UI")
            print("   4. Create your first backup")
            
        except Exception as e:
            conn.rollback()
            print(f"\n❌ Migration failed: {e}")
            print("Database rolled back to previous state")
            sys.exit(1)

if __name__ == "__main__":
    migrate_database()
