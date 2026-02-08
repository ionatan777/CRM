from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.message import Message
from app.services.whatsapp_backup import WhatsAppBackupService

router = APIRouter()

@router.get("/")
def get_messages(
    contact_phone: str = Query(None),
    limit: int = Query(500, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    View backed-up conversations (even if WhatsApp is down)
    VALUE: "Your messages are always accessible"
    """
    query = db.query(Message).filter(Message.user_id == current_user.id)
    
    if contact_phone:
        query = query.filter(Message.contact_phone == contact_phone)
    
    messages = query.order_by(Message.timestamp.desc()).limit(limit).all()
    
    return [
        {
            "id": str(msg.id),
            "contact_name": msg.contact_name,
            "contact_phone": msg.contact_phone,
            "message_text": msg.message_text,
            "message_type": msg.message_type,
            "timestamp": msg.timestamp.isoformat(),
            "is_from_me": msg.is_from_me
        }
        for msg in messages
    ]

@router.get("/search")
def search_messages(
    q: str = Query(..., min_length=2),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Search through ALL backed-up messages
    VALUE: "Find that conversation from 3 months ago in seconds"
    """
    service = WhatsAppBackupService("", "")
    results = service.search_messages(current_user.id, q, db)
    return results

@router.get("/contacts")
def get_contacts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of all contacts with backed-up messages"""
    from sqlalchemy import func, distinct
    
    contacts = db.query(
        Message.contact_phone,
        Message.contact_name,
        func.count(Message.id).label('message_count'),
        func.max(Message.timestamp).label('last_message_date')
    ).filter(
        Message.user_id == current_user.id
    ).group_by(
        Message.contact_phone, 
        Message.contact_name
    ).order_by(
        func.max(Message.timestamp).desc()
    ).all()
    
    return [
        {
            "contact_phone": c.contact_phone,
            "contact_name": c.contact_name,
            "message_count": c.message_count,
            "last_message_date": c.last_message_date.isoformat() if c.last_message_date else None
        }
        for c in contacts
    ]

@router.get("/export/{contact_phone}")
def export_conversation(
    contact_phone: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export complete conversation to PDF
    VALUE: "Legal documentation, audits, accounting records"
    """
    service = WhatsAppBackupService("", "")
    
    try:
        pdf_buffer = service.export_conversation_pdf(current_user.id, contact_phone, db)
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=conversacion_{contact_phone}.pdf"}
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")
