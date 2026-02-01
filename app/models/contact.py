from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.db.session import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=False, index=True)  # WhatsApp ID usually
    metadata_ = Column("metadata", JSONB, nullable=True) # avoiding reserved word clash if any
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    tenant = relationship("Tenant")
    conversations = relationship("Conversation", back_populates="contact")
    
    # New CRM features
    tags = relationship("Tag", secondary="contact_tags", back_populates="contacts")
    notes = relationship("Note", back_populates="contact")
