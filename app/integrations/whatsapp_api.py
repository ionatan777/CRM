"""
WhatsApp Business API Service (Pro Plan)
Integrates with Meta's official WhatsApp Business API
"""

import httpx
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.message import Message
from app.models.backup import Backup
from datetime import datetime, timedelta
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


class WhatsAppAPIService:
    """
    Service for Meta WhatsApp Business API (Pro Plan)
    Official API for businesses with unlimited messages
    """
    
    def __init__(self, phone_number_id: str, access_token: str):
        self.api_url = "https://graph.facebook.com/v18.0"
        self.phone_id = phone_number_id
        self.token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    async def fetch_messages(self, days_back: int = 30) -> List[Dict[str, Any]]:
        """
        Fetch messages from WhatsApp Business API
        Uses pagination to get all messages from the last X days
        
        Args:
            days_back: Number of days to look back for messages
            
        Returns:
            List of message dictionaries
        """
        logger.info(f"Fetching messages from WhatsApp API (last {days_back} days)")
        
        all_messages = []
        url = f"{self.api_url}/{self.phone_id}/messages"
        params = {"limit": 100}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            while True:
                try:
                    response = await client.get(url, headers=self.headers, params=params)
                    response.raise_for_status()
                    data = response.json()
                    
                    if "data" in data:
                        messages = data["data"]
                        all_messages.extend(messages)
                        logger.info(f"Fetched {len(messages)} messages")
                    
                    # Check for next page
                    if "paging" in data and "next" in data["paging"]:
                        url = data["paging"]["next"]
                        params = {}  # Next URL already has params
                    else:
                        break
                        
                except httpx.HTTPError as e:
                    logger.error(f"Error fetching messages: {e}")
                    break
        
        logger.info(f"Total messages fetched: {len(all_messages)}")
        return all_messages
    
    async def create_backup(self, user_id: UUID, db: Session) -> Dict[str, Any]:
        """
        Create a complete backup of WhatsApp conversations via Meta API
        
        Args:
            user_id: User ID to create backup for
            db: Database session
            
        Returns:
            Dictionary with backup results
        """
        logger.info(f"Creating WhatsApp API backup for user {user_id}")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        if not user.whatsapp_phone_id or not user.whatsapp_access_token:
            raise ValueError("WhatsApp API credentials not configured")
        
        # Create backup record
        backup = Backup(
            user_id=user_id,
            backup_date=datetime.utcnow(),
            status="in_progress",
            backup_source="api"  # Meta API
        )
        db.add(backup)
        db.commit()
        db.refresh(backup)
        
        try:
            # Fetch messages from API
            messages_data = await self.fetch_messages(days_back=90)
            
            # Save messages to database
            saved_count = 0
            contacts = set()
            
            for msg_data in messages_data:
                try:
                    # Extract message details from Meta API payload
                    from_number = msg_data.get("from", "")
                    contact_name = msg_data.get("profile", {}).get("name", "Unknown")
                    message_type = msg_data.get("type", "text")
                    
                    # Extract message text based on type
                    message_text = ""
                    if message_type == "text":
                        message_text = msg_data.get("text", {}).get("body", "")
                    elif message_type == "image":
                        message_text = f"[Image: {msg_data.get('image', {}).get('caption', 'No caption')}]"
                    elif message_type == "video":
                        message_text = f"[Video: {msg_data.get('video', {}).get('caption', 'No caption')}]"
                    elif message_type == "audio":
                        message_text = "[Audio message]"
                    elif message_type == "document":
                        message_text = f"[Document: {msg_data.get('document', {}).get('filename', 'Unknown')}]"
                    
                    # Create message record
                    message = Message(
                        user_id=user_id,
                        backup_id=backup.id,
                        whatsapp_message_id=msg_data.get("id"),
                        contact_name=contact_name,
                        contact_phone=from_number,
                        message_text=message_text,
                        message_type=message_type,
                        source="api",  # From Meta API
                        timestamp=datetime.fromtimestamp(int(msg_data.get("timestamp", 0))),
                        is_from_me=(from_number == user.phone_number)
                    )
                    db.add(message)
                    saved_count += 1
                    contacts.add(from_number)
                    
                except Exception as e:
                    logger.error(f"Error saving message: {e}")
                    continue
            
            # Update backup status
            backup.status = "completed"
            backup.total_messages = saved_count
            backup.total_contacts = len(contacts)
            db.commit()
            
            logger.info(f"Backup completed: {saved_count} messages, {len(contacts)} contacts")
            
            return {
                "backup_id": str(backup.id),
                "total_messages": saved_count,
                "total_contacts": len(contacts),
                "status": "completed",
                "backup_date": backup.backup_date.isoformat(),
                "source": "api"
            }
            
        except Exception as e:
            # Mark backup as failed
            backup.status = "failed"
            backup.error_message = str(e)
            db.commit()
            logger.error(f"Backup failed: {e}")
            raise
    
    async def send_test_message(self, to: str, message: str = "Test message from WhatsBackup") -> bool:
        """
        Send a test message to verify API connection
        
        Args:
            to: Phone number to send to (with country code, no +)
            message: Test message content
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Sending test message to {to}")
        
        url = f"{self.api_url}/{self.phone_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {
                "body": message
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                logger.info("Test message sent successfully")
                return True
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to send test message: {e}")
            return False
    
    async def verify_connection(self) -> Dict[str, Any]:
        """
        Verify that the API credentials are valid
        
        Returns:
            Dictionary with connection status and details
        """
        logger.info("Verifying WhatsApp API connection")
        
        url = f"{self.api_url}/{self.phone_id}"
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                
                return {
                    "connected": True,
                    "phone_number_id": self.phone_id,
                    "verified_name": data.get("verified_name", "Unknown"),
                    "quality_rating": data.get("quality_rating", "Unknown")
                }
                
        except httpx.HTTPError as e:
            logger.error(f"Connection verification failed: {e}")
            return {
                "connected": False,
                "error": str(e)
            }
