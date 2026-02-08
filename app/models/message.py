from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid
from datetime import datetime

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    backup_id = Column(UUID(as_uuid=True), ForeignKey("backups.id"), nullable=True)
    
    # WhatsApp message data
    whatsapp_message_id = Column(String, unique=True)
    contact_name = Column(String)
    contact_phone = Column(String, index=True)
    
    message_text = Column(Text)
    message_type = Column(String, default="text")  # text, image, video, audio, document
    source = Column(String, default="api")  # 'api' (Meta Business API) or 'baileys'
    
    timestamp = Column(DateTime, index=True)
    is_from_me = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="messages")
    backup = relationship("Backup", backref="messages")
    
    def __repr__(self):
        return f"<Message {self.id} from {self.contact_name}>"
