from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.whatsapp_backup import WhatsAppBackupService

router = APIRouter()

@router.post("/create")
async def create_backup_now(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create backup immediately (also runs automatically every 24hrs)
    VALUE PROP: "Backup now, sleep peacefully"
    """
    if not current_user.whatsapp_phone_id or not current_user.whatsapp_access_token:
        raise HTTPException(
            status_code=400, 
            detail="WhatsApp not connected. Please connect your WhatsApp Business account first."
        )
    
    service = WhatsAppBackupService(
        current_user.whatsapp_phone_id, 
        current_user.whatsapp_access_token
    )
    
    try:
        result = await service.create_backup(current_user.id, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backup failed: {str(e)}")

@router.get("/history")
def get_backup_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Show all backups performed"""
    service = WhatsAppBackupService("", "")  # No credentials needed for read operations
    backups = service.get_backup_history(current_user.id, db)
    return backups

@router.get("/stats")
def get_backup_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get overall backup statistics"""
    from app.models.backup import Backup
    from app.models.message import Message
    from sqlalchemy import func
    
    total_backups = db.query(func.count(Backup.id)).filter(
        Backup.user_id == current_user.id
    ).scalar()
    
    total_messages = db.query(func.count(Message.id)).filter(
        Message.user_id == current_user.id
    ).scalar()
    
    total_contacts = db.query(func.count(func.distinct(Message.contact_phone))).filter(
        Message.user_id == current_user.id
    ).scalar()
    
    last_backup = db.query(Backup).filter(
        Backup.user_id == current_user.id
    ).order_by(Backup.backup_date.desc()).first()
    
    return {
        "total_backups": total_backups or 0,
        "total_messages": total_messages or 0,
        "total_contacts": total_contacts or 0,
        "last_backup_date": last_backup.backup_date.isoformat() if last_backup else None
    }
