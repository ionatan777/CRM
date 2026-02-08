"""
WhatsBackup Core Service
Specialized in fetching, storing, and managing WhatsApp Business conversation backups
"""

import httpx
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.message import Message
from app.models.backup import Backup
from app.models.user import User
from typing import List, Dict, Any
import asyncio

class WhatsAppBackupService:
    """
    Service for backing up WhatsApp Business conversations
    VALUE PROP: "Your messages are safe even if WhatsApp fails"
    """
    
    def __init__(self, phone_number_id: str, access_token: str):
        self.api_url = "https://graph.facebook.com/v18.0"
        self.phone_id = phone_number_id
        self.token = access_token
    
    async def fetch_conversation_history(self, days_back: int = 30) -> List[Dict[str, Any]]:
        """
        Fetch complete message history from WhatsApp Business API
        Uses pagination to get ALL messages, not just recent ones
        """
        url = f"{self.api_url}/{self.phone_id}/messages"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        all_messages = []
        params = {"limit": 100}  # Max per request
        
        async with httpx.AsyncClient() as client:
            while True:
                try:
                    response = await client.get(url, headers=headers, params=params)
                    data = response.json()
                    
                    if "data" in data:
                        all_messages.extend(data["data"])
                    
                    # Check for next page
                    if "paging" in data and "next" in data["paging"]:
                        params["after"] = data["paging"]["cursors"]["after"]
                    else:
                        break
                except Exception as e:
                    print(f"Error fetching messages: {e}")
                    break
        
        return all_messages
    
    async def create_backup(self, user_id: int, db: Session) -> Dict[str, Any]:
        """
        Create complete backup of WhatsApp conversations
        CORE FEATURE - This is what customers pay for
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise ValueError("User not found")
        
        if not user.whatsapp_phone_id or not user.whatsapp_access_token:
            raise ValueError("User doesn't have WhatsApp connected")
        
        # Fetch messages from WhatsApp
        messages_data = await self.fetch_conversation_history(days_back=90)
        
        # Create backup record
        backup = Backup(
            user_id=user_id,
            backup_date=datetime.utcnow(),
            status="in_progress"
        )
        db.add(backup)
        db.commit()
        db.refresh(backup)
        
        # Save messages to database (PERSISTENT BACKUP)
        saved_count = 0
        contacts = set()
        
        for msg_data in messages_data:
            try:
                # Extract message details from WhatsApp payload
                from_data = msg_data.get("from", {})
                contact_phone = from_data if isinstance(from_data, str) else from_data.get("phone", "")
                
                message = Message(
                    user_id=user_id,
                    backup_id=backup.id,
                    whatsapp_message_id=msg_data.get("id"),
                    contact_name=msg_data.get("profile", {}).get("name", "Unknown"),
                    contact_phone=contact_phone,
                    message_text=msg_data.get("text", {}).get("body", ""),
                    message_type=msg_data.get("type", "text"),
                    timestamp=datetime.fromtimestamp(int(msg_data.get("timestamp", 0))),
                    is_from_me=contact_phone == user.phone_number
                )
                db.add(message)
                saved_count += 1
                contacts.add(contact_phone)
            except Exception as e:
                print(f"Error saving message: {e}")
                continue
        
        # Mark backup as completed
        backup.status = "completed"
        backup.total_messages = saved_count
        backup.total_contacts = len(contacts)
        db.commit()
        
        return {
            "backup_id": str(backup.id),
            "total_messages": saved_count,
            "total_contacts": len(contacts),
            "status": "completed",
            "backup_date": backup.backup_date.isoformat()
        }
    
    def get_backup_history(self, user_id: int, db: Session) -> List[Dict[str, Any]]:
        """Mostrar historial de backups realizados"""
        backups = db.query(Backup).filter(
            Backup.user_id == user_id
        ).order_by(Backup.backup_date.desc()).all()
        
        return [
            {
                "id": str(backup.id),
                "backup_date": backup.backup_date.isoformat(),
                "total_messages": backup.total_messages,
                "total_contacts": backup.total_contacts,
                "status": backup.status
            }
            for backup in backups
        ]
    
    def search_messages(self, user_id: int, query: str, db: Session) -> List[Dict[str, Any]]:
        """
        Search through backed-up messages
        VALUE: "Find any conversation from months ago in seconds"
        """
        messages = db.query(Message).filter(
            Message.user_id == user_id,
            Message.message_text.ilike(f"%{query}%")
        ).order_by(Message.timestamp.desc()).limit(100).all()
        
        return [
            {
                "id": str(msg.id),
                "contact_name": msg.contact_name,
                "contact_phone": msg.contact_phone,
                "message_text": msg.message_text,
                "timestamp": msg.timestamp.isoformat(),
                "is_from_me": msg.is_from_me
            }
            for msg in messages
        ]
    
    def export_conversation_pdf(self, user_id: int, contact_phone: str, db: Session):
        """
        Export complete conversation to PDF
        VALUE: "Legal documentation, audits, accounting records"
        """
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from io import BytesIO
        
        messages = db.query(Message).filter(
            Message.user_id == user_id,
            Message.contact_phone == contact_phone
        ).order_by(Message.timestamp).all()
        
        if not messages:
            raise ValueError("No messages found for this contact")
        
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        
        # Header
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 750, f"Conversacion con {messages[0].contact_name}")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, 730, f"Total mensajes: {len(messages)}")
        pdf.drawString(50, 715, f"Exportado: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Messages
        y_position = 680
        for msg in messages:
            if y_position < 50:
                pdf.showPage()
                y_position = 750
            
            sender = "Yo" if msg.is_from_me else msg.contact_name
            timestamp = msg.timestamp.strftime("%Y-%m-%d %H:%M")
            
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawString(50, y_position, f"{sender} - {timestamp}")
            y_position -= 15
            
            pdf.setFont("Helvetica", 9)
            # Word wrap for long messages
            text = msg.message_text[:200] + "..." if len(msg.message_text) > 200 else msg.message_text
            pdf.drawString(70, y_position, text)
            y_position -= 25
        
        pdf.save()
        buffer.seek(0)
        return buffer
