from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    phone_number = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Plan Information
    plan_type = Column(String, default='express')  # 'express' or 'pro'
    plan_status = Column(String, default='trial')  # 'trial', 'active', 'cancelled'
    
    # WhatsApp Business API Credentials (Pro Plan)
    whatsapp_phone_id = Column(String, nullable=True)
    whatsapp_access_token = Column(String, nullable=True)
    
    # Baileys Session (Express Plan)
    baileys_session_id = Column(String, nullable=True)
    baileys_auth_state = Column(Text, nullable=True)
    
    # Auto-backup settings
    auto_backup_enabled = Column(Boolean, default=True)
    backup_frequency_hours = Column(Integer, default=24)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<User {self.email}>"
