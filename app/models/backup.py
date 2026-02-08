from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid
from datetime import datetime

class Backup(Base):
    __tablename__ = "backups"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    backup_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="in_progress")  # in_progress, completed, failed
    backup_source = Column(String, default="api")  # 'api' (Meta) or 'baileys'
    
    total_messages = Column(Integer, default=0)
    total_contacts = Column(Integer, default=0)
    
    error_message = Column(String, nullable=True)
    
    # Relationships
    user = relationship("User", backref="backups")
    
    def __repr__(self):
        return f"<Backup {self.id} - {self.status}>"
