from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.messaging import MessagingService
from app.schemas.message import MessageSend
from app.api.deps import get_current_user
import uuid

router = APIRouter()

@router.post("/", status_code=201)
async def send_message(
    message: MessageSend,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = MessagingService(db)
    try:
        sent_msg = await service.send_outbound_message(
            tenant_id=current_user.tenant_id,
            contact_id=message.contact_id,
            content=message.content
        )
        return {"id": sent_msg.id, "status": "sent"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
