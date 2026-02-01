from pydantic import BaseModel, UUID4
from typing import Optional, Dict, Any, List
from app.schemas.crm import TagOut, NoteOut

class ContactBase(BaseModel):
    name: Optional[str] = None
    phone: str
    metadata_: Optional[Dict[str, Any]] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    phone: Optional[str] = None

class ContactInDBBase(ContactBase):
    id: UUID4
    tenant_id: UUID4
    tags: List[TagOut] = []
    notes: List[NoteOut] = []

    class Config:
        from_attributes = True

class Contact(ContactInDBBase):
    pass
