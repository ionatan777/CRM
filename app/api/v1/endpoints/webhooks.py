from fastapi import APIRouter, Depends, Request, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.messaging import MessagingService
from app.infrastructure.whatsapp.meta_provider import MetaProvider
import uuid

router = APIRouter()

# For MVP, we use a single hardcoded tenant for webhooks or extract from path
# But standard WhatsApp webhooks don't pass tenant_id. 
# Usually you map Phone Number ID -> Tenant in a config table.
# For this MVP, we will assume a constant Tenant ID (the one we seeded or passed in logic).
FIXED_TENANT_ID = uuid.UUID("47f61e5d-0d94-4961-b4e8-5ef09db11934") 

@router.get("/whatsapp")
def verify_webhook(
    mode: str = Query(alias="hub.mode"),
    token: str = Query(alias="hub.verify_token"),
    challenge: str = Query(alias="hub.challenge")
):
    provider = MetaProvider()
    if mode == "subscribe" and provider.verify_webhook_token(token):
        return int(challenge)
    raise HTTPException(status_code=403, detail="Verification failed")

@router.post("/whatsapp")
async def handle_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    payload = await request.json()
    service = MessagingService(db)
    
    # In a real app we would lookup which Tenant owns the "entry.changes.value.metadata.phone_number_id"
    result = service.process_incoming_webhook(payload, FIXED_TENANT_ID)
    
    return result
