from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.db.session import engine, Base
from app.models.tenant import Tenant
from app.models.contact import Contact
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.tag import Tag
from app.models.note import Note 
from app.models.backup import BackupJob
from app.models.user import User # Import all models so they are registered

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

from app.core.middleware import AuditMiddleware
app.add_middleware(AuditMiddleware)

from app.api.v1.endpoints import contacts, webhooks, messages, conversations, backups, auth

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(contacts.router, prefix="/api/v1/contacts", tags=["contacts"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["webhooks"])
app.include_router(messages.router, prefix="/api/v1/messages", tags=["messages"])
app.include_router(conversations.router, prefix="/api/v1/conversations", tags=["conversations"])
app.include_router(backups.router, prefix="/api/v1/backups", tags=["backups"])

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "0.1.0"}

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
