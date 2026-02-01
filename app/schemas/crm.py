from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import datetime

class TagBase(BaseModel):
    name: str
    color: Optional[str] = "#CCCCCC"

class TagCreate(TagBase):
    pass

class TagOut(TagBase):
    id: UUID4
    class Config:
        from_attributes = True

class NoteBase(BaseModel):
    content: str

class NoteCreate(NoteBase):
    pass

class NoteOut(NoteBase):
    id: UUID4
    created_at: datetime
    class Config:
        from_attributes = True
