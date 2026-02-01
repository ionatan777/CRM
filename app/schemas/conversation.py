from pydantic import BaseModel, UUID4
from typing import Optional, List, Any
from datetime import datetime
from app.schemas.contact import Contact

class MessageOut(BaseModel):
    id: UUID4
    content: str
    direction: str
    type: str
    created_at: datetime
    is_read: bool

    class Config:
        from_attributes = True

class ConversationListOut(BaseModel):
    id: UUID4
    contact: Contact
    last_message: Optional[str] = None
    last_message_at: Optional[datetime] = None
    unread_count: int = 0
    status: str

    class Config:
        from_attributes = True
