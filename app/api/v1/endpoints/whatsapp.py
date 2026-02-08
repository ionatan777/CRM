from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.whatsapp_backup import WhatsAppBackupService
from app.integrations.whatsapp_api import WhatsAppAPIService
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class WhatsAppConnect(BaseModel):
    phone_number_id: str
    access_token: str

@router.post("/connect")
async def connect_whatsapp(
    data: WhatsAppConnect,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Connect user's WhatsApp Business account (Pro Plan)
    THE MAGIC MOMENT: "From now on, you're protected"
    """
    # Verify credentials are valid first
    service = WhatsAppAPIService(data.phone_number_id, data.access_token)
    verification = await service.verify_connection()
    
    if not verification.get("connected"):
        raise HTTPException(
            status_code=400, 
            detail="Invalid WhatsApp credentials. Please check your Phone Number ID and Access Token."
        )
    
    # Save credentials
    current_user.whatsapp_phone_id = data.phone_number_id
    current_user.whatsapp_access_token = data.access_token
    current_user.plan_type = 'pro'  # Ensure user is on Pro plan
    db.commit()
    
    logger.info(f"User {current_user.email} connected WhatsApp Pro successfully")
    
    return {
        "status": "connected",
        "message": "WhatsApp conectado. Tu primer backup se creará automáticamente.",
        "verified_name": verification.get("verified_name"),
        "quality_rating": verification.get("quality_rating")
    }

@router.get("/status")
async def get_whatsapp_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if WhatsApp Pro is connected and verify status"""
    is_connected = bool(current_user.whatsapp_phone_id and current_user.whatsapp_access_token)
    
    result = {
        "connected": is_connected,
        "phone_id": current_user.whatsapp_phone_id if is_connected else None,
        "plan_type": current_user.plan_type
    }
    
    # If connected, verify the connection is still valid
    if is_connected:
        try:
            service = WhatsAppAPIService(
                current_user.whatsapp_phone_id,
                current_user.whatsapp_access_token
            )
            verification = await service.verify_connection()
            result["verified"] = verification.get("connected", False)
            result["verified_name"] = verification.get("verified_name")
        except Exception as e:
            logger.error(f"Failed to verify connection: {e}")
            result["verified"] = False
            result["error"] = "Connection verification failed"
    
    return result

@router.post("/create-backup")
async def create_manual_backup(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create manual backup for Pro plan user"""
    if current_user.plan_type != 'pro':
        raise HTTPException(
            status_code=403,
            detail="This feature is only available for Pro plan users"
        )
    
    if not current_user.whatsapp_phone_id or not current_user.whatsapp_access_token:
        raise HTTPException(
            status_code=400,
            detail="WhatsApp not connected. Please connect first."
        )
    
    try:
        service = WhatsAppAPIService(
            current_user.whatsapp_phone_id,
            current_user.whatsapp_access_token
        )
        result = await service.create_backup(current_user.id, db)
        return result
    except Exception as e:
        logger.error(f"Manual backup failed for {current_user.email}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/disconnect")
async def disconnect_whatsapp(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Disconnect WhatsApp Pro"""
    current_user.whatsapp_phone_id = None
    current_user.whatsapp_access_token = None
    db.commit()
    
    return {
        "status": "disconnected",
        "message": "WhatsApp disconnected successfully"
    }
