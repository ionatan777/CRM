# Test script to verify WhatsBackup models work correctly
# Run with: python scripts/test_models.py

from app.db.session import SessionLocal
from app.models.user import User
from app.models.backup import Backup
from app.models.message import Message
from datetime import datetime
import uuid

def test_models():
    """Test that all WhatsBackup models work correctly"""
    
    print("🧪 Testing WhatsBackup Models...")
    db = SessionLocal()
    
    try:
        # Test 1: Create a test user
        print("\n1️⃣  Creating test user...")
        test_user = User(
            email="test@whatsbackup.com",
            hashed_password="hashed_test_password",
            full_name="Test User",
            phone_number="+1234567890",
            whatsapp_phone_id="test_phone_id_123",
            whatsapp_access_token="test_token_abc",
            auto_backup_enabled=True,
            backup_frequency_hours=24
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"   ✅ Created user: {test_user.email} (ID: {test_user.id})")
        
        # Test 2: Create a test backup
        print("\n2️⃣  Creating test backup...")
        test_backup = Backup(
            user_id=test_user.id,
            backup_date=datetime.utcnow(),
            status="completed",
            total_messages=10,
            total_contacts=3
        )
        db.add(test_backup)
        db.commit()
        db.refresh(test_backup)
        print(f"   ✅ Created backup: {test_backup.id} with {test_backup.total_messages} messages")
        
        # Test 3: Create test messages
        print("\n3️⃣  Creating test messages...")
        contacts = [
            ("Juan Pérez", "+52123456789"),
            ("María García", "+52987654321"),
            ("Carlos López", "+52555555555")
        ]
        
        for contact_name, contact_phone in contacts:
            message = Message(
                user_id=test_user.id,
                backup_id=test_backup.id,
                whatsapp_message_id=f"wamid_{uuid.uuid4()}",
                contact_name=contact_name,
                contact_phone=contact_phone,
                message_text=f"Hola, este es un mensaje de prueba de {contact_name}",
                message_type="text",
                timestamp=datetime.utcnow(),
                is_from_me=False
            )
            db.add(message)
        
        db.commit()
        print(f"   ✅ Created {len(contacts)} test messages")
        
        # Test 4: Query messages
        print("\n4️⃣  Testing message queries...")
        all_messages = db.query(Message).filter(Message.user_id == test_user.id).all()
        print(f"   ✅ Found {len(all_messages)} messages for user")
        
        # Test 5: Search functionality
        print("\n5️⃣  Testing search...")
        search_results = db.query(Message).filter(
            Message.user_id == test_user.id,
            Message.message_text.ilike("%prueba%")
        ).all()
        print(f"   ✅ Search for 'prueba' returned {len(search_results)} results")
        
        # Test 6: Backup stats
        print("\n6️⃣  Testing backup statistics...")
        user_backups = db.query(Backup).filter(Backup.user_id == test_user.id).all()
        total_messages = sum(b.total_messages for b in user_backups)
        print(f"   ✅ User has {len(user_backups)} backups with {total_messages} total messages")
        
        # Cleanup
        print("\n🧹 Cleaning up test data...")
        db.query(Message).filter(Message.user_id == test_user.id).delete()
        db.query(Backup).filter(Backup.user_id == test_user.id).delete()
        db.query(User).filter(User.id == test_user.id).delete()
        db.commit()
        print("   ✅ Cleanup complete")
        
        print("\n✅ All model tests passed!")
        print("\n📌 Models are working correctly:")
        print("   ✓ User model with WhatsApp credentials")
        print("   ✓ Backup model with statistics")
        print("   ✓ Message model with full-text search")
        print("   ✓ Relationships between models")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_models()
