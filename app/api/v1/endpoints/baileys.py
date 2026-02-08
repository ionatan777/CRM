"""
Baileys API Endpoints (Express Plan)
Handles WhatsApp connections via QR code for Express plan users
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.integrations.whatsapp_baileys import BaileysService
from pydantic import BaseModel
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize Baileys service
baileys_service = BaileysService()


class QRResponse(BaseModel):
    """Response model for QR generation"""
    session_id: str
    qr_code: str
    status: str
    message: str
    expires_in: int


class ConnectionStatus(BaseModel):
    """Response model for connection status"""
    connected: bool
    session_id: str = None
    status: str = None


def verify_express_plan(current_user: User):
    """Middleware to verify user is on Express plan"""
    if current_user.plan_type != 'express':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This feature is only available for Express plan users. You're on the Pro plan."
        )


@router.post("/generate-qr", response_model=QRResponse)
async def generate_qr_code(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate QR code for WhatsApp connection (Express plan only)
    
    Returns QR code image (base64) that user scans with WhatsApp
    """
    # Verify Express plan
    verify_express_plan(current_user)
    
    logger.info(f"Generating QR code for user {current_user.email} (Express plan)")
    
    try:
        result = await baileys_service.generate_qr_code(current_user.id, db)
        return result
        
    except Exception as e:
        logger.error(f"Failed to generate QR: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate QR code: {str(e)}"
        )


@router.get("/status", response_model=ConnectionStatus)
async def check_connection_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check if WhatsApp is connected for current user
    
    Frontend should poll this endpoint after showing QR to check if user scanned it
    """
    verify_express_plan(current_user)
    
    try:
        status_data = await baileys_service.check_connection_status(current_user.id, db)
        return status_data
        
    except Exception as e:
        logger.error(f"Failed to check status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check connection status: {str(e)}"
        )


@router.post("/create-backup")
async def create_backup(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create manual backup from Baileys session (Express plan)
    
    Fetches all messages from connected WhatsApp Web session and saves to database
    """
    verify_express_plan(current_user)
    
    logger.info(f"Creating Baileys backup for user {current_user.email}")
    
    # Check if user can create backup (check message limits)
    from app.services.plans import can_create_backup
    can_backup, reason = can_create_backup(current_user.id, db)
    
    if not can_backup:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=reason
        )
    
    try:
        result = await baileys_service.create_backup(current_user.id, db)
        
        # Increment message count for Express plan
        from app.services.plans import increment_message_count
        increment_message_count(current_user.id, result['total_messages'], db)
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to create backup: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Backup failed: {str(e)}"
        )


@router.delete("/disconnect")
async def disconnect_session(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Disconnect WhatsApp session (logout)
    
    User will need to scan QR again to reconnect
    """
    verify_express_plan(current_user)
    
    logger.info(f"Disconnecting Baileys session for user {current_user.email}")
    
    try:
        success = await baileys_service.disconnect_session(current_user.id, db)
        
        if success:
            return {
                "message": "WhatsApp disconnected successfully",
                "status": "disconnected"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active session found"
            )
            
    except Exception as e:
        logger.error(f"Failed to disconnect: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to disconnect: {str(e)}"
        )
