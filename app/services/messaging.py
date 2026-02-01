from sqlalchemy.orm import Session
from app.models.contact import Contact
from app.models.conversation import Conversation, ConversationStatus
from app.models.message import Message, MessageDirection, MessageType
from app.infrastructure.whatsapp.meta_provider import MetaProvider
from app.core.interfaces.provider import WhatsAppProvider
import uuid

class MessagingService:
    def __init__(self, db: Session, provider: WhatsAppProvider = None):
        self.db = db
        self.provider = provider or MetaProvider()

    def process_incoming_webhook(self, payload: dict, tenant_id: uuid.UUID):
        """
        Extracts message info from Meta payload and saves it.
        This assumes a standard Meta structure (entry -> changes -> value -> messages).
        """
        # 1. Normalize Payload (Simplified for MVP)
        try:
            entry = payload.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            
            if not messages:
                return {"status": "no_messages"}

            msg_data = messages[0]
            sender_phone = msg_data.get("from")
            msg_type = msg_data.get("type")
            
            # Extract content based on type
            content = ""
            if msg_type == "text":
                content = msg_data.get("text", {}).get("body", "")
            else:
                content = f"[{msg_type.upper()}]"

            # 2. Find or Create Contact
            contact = self.db.query(Contact).filter(
                Contact.phone == sender_phone, 
                Contact.tenant_id == tenant_id
            ).first()

            if not contact:
                contact = Contact(
                    phone=sender_phone,
                    tenant_id=tenant_id,
                    name=value.get("contacts", [{}])[0].get("profile", {}).get("name", "Unknown")
                )
                self.db.add(contact)
                self.db.commit()
                self.db.refresh(contact)

            # 3. Find or Create Open Conversation
            conversation = self.db.query(Conversation).filter(
                Conversation.contact_id == contact.id,
                Conversation.tenant_id == tenant_id,
                Conversation.status == ConversationStatus.OPEN
            ).first()

            if not conversation:
                conversation = Conversation(
                    contact_id=contact.id,
                    tenant_id=tenant_id,
                    status=ConversationStatus.OPEN
                )
                self.db.add(conversation)
                self.db.commit()
                self.db.refresh(conversation)

            # 4. Save Message
            new_message = Message(
                conversation_id=conversation.id,
                content=content,
                direction=MessageDirection.INBOUND,
                type=MessageType(msg_type) if msg_type in ["text", "image"] else MessageType.TEXT
            )
            self.db.add(new_message)
            self.db.commit()
            
            return {"status": "processed", "message_id": new_message.id}

        except Exception as e:
            print(f"Error processing webhook: {e}")
            return {"status": "error", "detail": str(e)}

    async def send_outbound_message(self, tenant_id: uuid.UUID, contact_id: uuid.UUID, content: str):
         # 1. Get Contact
        contact = self.db.query(Contact).filter(Contact.id == contact_id, Contact.tenant_id == tenant_id).first()
        if not contact:
            raise ValueError("Contact not found")

        # 2. Get Open Conversation or Create
        conversation = self.db.query(Conversation).filter(
            Conversation.contact_id == contact.id,
            Conversation.tenant_id == tenant_id,
             Conversation.status == ConversationStatus.OPEN
        ).first()

        if not conversation:
             conversation = Conversation(
                contact_id=contact.id,
                tenant_id=tenant_id,
                status=ConversationStatus.OPEN
            )
             self.db.add(conversation)
             self.db.commit()
             self.db.refresh(conversation)

        # 3. Send via Provider
        provider_response = await self.provider.send_message(to=contact.phone, content=content)

        # 4. Save Message in DB
        new_message = Message(
            conversation_id=conversation.id,
            content=content,
            direction=MessageDirection.OUTBOUND,
            type=MessageType.TEXT
        )
        self.db.add(new_message)
        self.db.commit()

        return new_message
