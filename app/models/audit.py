from sqlalchemy import Column, String, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.db.session import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True) # nullable for system actions or failed auth
    tenant_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    action = Column(String, nullable=False, index=True) # POST, PUT, DELETE, LOGIN
    resource = Column(String, nullable=False, index=True) # contacts, messages
    details = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
