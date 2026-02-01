from pydantic import BaseModel, UUID4

class MessageSend(BaseModel):
    contact_id: UUID4
    content: str
