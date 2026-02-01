from sqlalchemy.orm import Session
from app.models.backup import BackupJob, BackupStatus
from app.models.contact import Contact
from app.models.conversation import Conversation
from app.models.message import Message
from app.core.interfaces.storage import StorageProvider
from app.infrastructure.storage.local import LocalStorageProvider
import json
import uuid
from datetime import datetime

# Helper for datetime serialization
def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

class BackupService:
    def __init__(self, db: Session, storage: StorageProvider = None):
        self.db = db
        self.storage = storage or LocalStorageProvider()

    def perform_backup(self, tenant_id: uuid.UUID, job_id: uuid.UUID):
        try:
            # 1. Fetch Data
            contacts = self.db.query(Contact).filter(Contact.tenant_id == tenant_id).all()
            
            # Serialize Data Structure
            data = {
                "tenant_id": str(tenant_id),
                "created_at": datetime.now().isoformat(),
                "contacts": []
            }

            for contact in contacts:
                contact_data = {
                    "id": str(contact.id),
                    "name": contact.name,
                    "phone": contact.phone,
                    "tags": [t.name for t in contact.tags],
                    "notes": [{"content": n.content, "date": n.created_at} for n in contact.notes],
                    "conversations": []
                }
                
                # Nested Conversations
                for conv in contact.conversations:
                    conv_data = {
                        "id": str(conv.id),
                        "status": conv.status,
                        "messages": []
                    }
                    
                    # Nested Messages
                    for msg in conv.messages:
                        conv_data["messages"].append({
                            "direction": msg.direction,
                            "type": msg.type,
                            "content": msg.content,
                            "is_read": msg.is_read,
                            "timestamp": msg.created_at
                        })
                    
                    contact_data["conversations"].append(conv_data)
                
                data["contacts"].append(contact_data)

            # 2. Save File
            filename = f"backup_{tenant_id}_{job_id}.json"
            json_bytes = json.dumps(data, default=json_serial, indent=2).encode('utf-8')
            file_path = self.storage.save_file(filename, json_bytes)

            # 3. Update Job Status
            job = self.db.query(BackupJob).filter(BackupJob.id == job_id).first()
            if job:
                job.status = BackupStatus.COMPLETED
                job.file_path = file_path
                self.db.commit()

        except Exception as e:
            print(f"Backup Failed: {e}")
            job = self.db.query(BackupJob).filter(BackupJob.id == job_id).first()
            if job:
                job.status = BackupStatus.FAILED
                self.db.commit()
