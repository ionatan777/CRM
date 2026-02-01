from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, case
from app.db.session import get_db
from app.models.conversation import Conversation
from app.models.message import Message, MessageDirection
from app.models.contact import Contact
from app.schemas.conversation import ConversationListOut, MessageOut
from app.api.deps import get_current_user
import uuid

router = APIRouter()

@router.get("/", response_model=list[ConversationListOut])
def list_conversations(
    skip: int = 0,
    limit: int = 50,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List conversations for a tenant, ordered by last activity.
    Includes unread count calculation.
    """
    conversations = db.query(Conversation).filter(
        Conversation.tenant_id == current_user.tenant_id
    ).order_by(desc(Conversation.last_message_at)).offset(skip).limit(limit).all()

    results = []
    for conv in conversations:
        # Calculate unread messages (Inbound only)
        unread = db.query(func.count(Message.id)).filter(
            Message.conversation_id == conv.id,
            Message.direction == MessageDirection.INBOUND,
            Message.is_read == False
        ).scalar()
        
        # Get last message content
        last_msg = db.query(Message).filter(Message.conversation_id == conv.id).order_by(desc(Message.created_at)).first()

        results.append({
            "id": conv.id,
            "contact": conv.contact,
            "status": conv.status,
            "last_message": last_msg.content if last_msg else None,
            "last_message_at": conv.last_message_at,
            "unread_count": unread
        })
    
    return results

@router.get("/{conversation_id}/messages", response_model=list[MessageOut])
def list_messages(
    conversation_id: str,
    skip: int = 0,
    limit: int = 50,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify access
    conv = db.query(Conversation).filter(
        Conversation.id == uuid.UUID(conversation_id), 
        Conversation.tenant_id == current_user.tenant_id
    ).first()
    
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = db.query(Message).filter(
        Message.conversation_id == conv.id
    ).order_by(func.created_at()).offset(skip).limit(limit).all()
    
    return messages

@router.post("/{conversation_id}/read")
def mark_as_read(
    conversation_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv = db.query(Conversation).filter(
        Conversation.id == uuid.UUID(conversation_id), 
        Conversation.tenant_id == current_user.tenant_id
    ).first()

    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    # Update unread messages
    db.query(Message).filter(
        Message.conversation_id == conv.id,
        Message.direction == MessageDirection.INBOUND,
        Message.is_read == False
    ).update({"is_read": True})
    
    db.commit()
    return {"status": "ok"}
