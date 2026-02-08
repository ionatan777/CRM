"""
Baileys Python Bridge (Express Plan)
Python wrapper to communicate with Baileys Node.js server
"""

import httpx
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.message import Message
from app.models.backup import Backup
from datetime import datetime
from uuid import UUID
import logging
import asyncio

logger = logging.getLogger(__name__)


class BaileysService:
    """
    Service to interact with Baileys Node.js server
    Used for Express plan (WhatsApp Web via QR)
    """
    
    def __init__(self, baileys_server_url: str = "http://localhost:3000"):
        self.server_url = baileys_server_url
        self.timeout = httpx.Timeout(30.0, connect=10.0)
    
    async def generate_qr_code(self, user_id: UUID, db: Session) -> Dict[str, Any]:
        """
        Generate QR code for WhatsApp connection
        
        Args:
            user_id: User ID to generate QR for
            db: Database session
            
        Returns:
            Dictionary with QR code data (base64 image)
        """
        logger.info(f"Generating QR code for user {user_id}")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Create unique session ID
        session_id = str(user_id)
        
        # Call Baileys server to generate QR
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.server_url}/generate-qr",
                    json={"session_id": session_id}
                )
                response.raise_for_status()
                data = response.json()
                
                # Save session ID to user
                user.baileys_session_id = session_id
                db.commit()
                
                logger.info(f"QR generated successfully for {user_id}")
                return data
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to generate QR: {e}")
            raise Exception(f"Baileys server error: {str(e)}")
    
    async def check_connection_status(self, user_id: UUID, db: Session) -> Dict[str, Any]:
        """
        Check if WhatsApp is connected for this user
        
        Args:
            user_id: User ID to check
            db: Database session
            
        Returns:
            Dictionary with connection status
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.baileys_session_id:
            return {"connected": False, "reason": "No session found"}
        
        session_id = user.baileys_session_id
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.server_url}/status/{session_id}"
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to check status: {e}")
            return {"connected": False, "error": str(e)}
    
    async def fetch_messages(self, user_id: UUID, days_back: int = 30) -> List[Dict[str, Any]]:
        """
        Fetch messages from Baileys session
        
        Args:
            user_id: User ID
            days_back: Number of days to look back
            
        Returns:
            List of messages
        """
        logger.info(f"Fetching messages from Baileys for user {user_id}")
        
        from app.db.session import SessionLocal
        db = SessionLocal()
        
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user or not user.baileys_session_id:
                raise ValueError("No Baileys session found for user")
            
            session_id = user.baileys_session_id
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.server_url}/fetch-messages",
                    json={"session_id": session_id, "days_back": days_back}
                )
                response.raise_for_status()
                data = response.json()
                
                messages = data.get("messages", [])
                logger.info(f"Fetched {len(messages)} messages from Baileys")
                return messages
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch messages: {e}")
            raise
        finally:
            db.close()
    
    async def create_backup(self, user_id: UUID, db: Session) -> Dict[str, Any]:
        """
        Create backup from Baileys session
        
        Args:
            user_id: User ID
            db: Database session
            
        Returns:
            Backup results dictionary
        """
        logger.info(f"Creating Baileys backup for user {user_id}")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        if not user.baileys_session_id:
            raise ValueError("No Baileys session found. Please connect WhatsApp first.")
        
        # Check connection status
        status = await self.check_connection_status(user_id, db)
        if not status.get("connected"):
            raise ValueError("WhatsApp is not connected. Please scan QR code again.")
        
        # Create backup record
        backup = Backup(
            user_id=user_id,
            backup_date=datetime.utcnow(),
            status="in_progress",
            backup_source="baileys"  # From Baileys
        )
        db.add(backup)
        db.commit()
        db.refresh(backup)
        
        try:
            # Fetch messages from Baileys
            messages_data = await self.fetch_messages(user_id, days_back=90)
            
            # Save messages to database
            saved_count = 0
            contacts = set()
            
            for msg_data in messages_data:
                try:
                    contact_phone = msg_data.get("from", "")
                    
                    message = Message(
                        user_id=user_id,
                        backup_id=backup.id,
                        whatsapp_message_id=msg_data.get("id"),
                        contact_name="Unknown",  # Baileys doesn't provide names easily
                        contact_phone=contact_phone,
                        message_text=msg_data.get("text", ""),
                        message_type="text",
                        source="baileys",  # From Baileys
                        timestamp=datetime.fromtimestamp(int(msg_data.get("timestamp", 0))),
                        is_from_me=msg_data.get("from_me", False)
                    )
                    db.add(message)
                    saved_count += 1
                    contacts.add(contact_phone)
                    
                except Exception as e:
                    logger.error(f"Error saving message: {e}")
                    continue
            
            # Update backup status
            backup.status = "completed"
            backup.total_messages = saved_count
            backup.total_contacts = len(contacts)
            db.commit()
            
            logger.info(f"Baileys backup completed: {saved_count} messages")
            
            return {
                "backup_id": str(backup.id),
                "total_messages": saved_count,
                "total_contacts": len(contacts),
                "status": "completed",
                "backup_date": backup.backup_date.isoformat(),
                "source": "baileys"
            }
            
        except Exception as e:
            # Mark backup as failed
            backup.status = "failed"
            backup.error_message = str(e)
            db.commit()
            logger.error(f"Baileys backup failed: {e}")
            raise
    
    async def disconnect_session(self, user_id: UUID, db: Session) -> bool:
        """
        Disconnect Baileys session (logout)
        
        Args:
            user_id: User ID
            db: Database session
            
        Returns:
            True if successful
        """
        logger.info(f"Disconnecting Baileys session for user {user_id}")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.baileys_session_id:
            return False
        
        session_id = user.baileys_session_id
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.server_url}/disconnect/{session_id}"
                )
                response.raise_for_status()
                
                # Clear session from user
                user.baileys_session_id = None
                user.baileys_auth_state = None
                db.commit()
                
                logger.info(f"Session disconnected successfully for {user_id}")
                return True
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to disconnect: {e}")
            return False
