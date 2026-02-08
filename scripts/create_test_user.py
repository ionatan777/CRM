"""
Script para crear usuario de prueba en WhatsBackup
Ejecutar con: python scripts/create_test_user.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def create_test_user():
    """Crear usuario de prueba para WhatsBackup"""
    db = SessionLocal()
    
    try:
        # Verificar si el usuario ya existe
        existing = db.query(User).filter(User.email == "test@whatsbackup.com").first()
        if existing:
            print("❌ El usuario test@whatsbackup.com ya existe")
            print(f"   Puedes usar: test@whatsbackup.com / test123")
            return
        
        # Crear nuevo usuario
        test_user = User(
            email="test@whatsbackup.com",
            hashed_password=get_password_hash("test123"),
            full_name="Usuario Test",
            phone_number="+573001234567",
            plan_type="express",  # Plan Express por defecto
            plan_status="trial",
            auto_backup_enabled=True,
            backup_frequency_hours=12
        )
        
        db.add(test_user)
        db.commit()
        
        print("✅ ¡Usuario creado exitosamente!")
        print("\n📧 Credenciales de acceso:")
        print("   Email: test@whatsbackup.com")
        print("   Password: test123")
        print("\n🚀 Puedes iniciar sesión en: http://localhost:5173")
        
    except Exception as e:
        print(f"❌ Error al crear usuario: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
