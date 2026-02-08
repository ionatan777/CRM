from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.db.session import engine, Base
from app.models.user import User
from app.models.message import Message
from app.models.backup import Backup
from app.models.subscription import Subscription
import asyncio
import logging

logger = logging.getLogger(__name__)

# Import all models so they are registered


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    
    # Start background schedulers
    logger.info("🚀 Starting automated backup schedulers...")
    
    # Start Express backup scheduler (every 12 hours)
    from app.schedulers.express_backup import run_express_backup
    asyncio.create_task(schedule_express_backups(run_express_backup))
    
    # Start Pro backup scheduler (every 24 hours)
    from app.schedulers.pro_backup import run_pro_backup
    asyncio.create_task(schedule_pro_backups(run_pro_backup))
    
    logger.info("✅ Schedulers started successfully")
    
    yield
    
    logger.info("Shutting down schedulers...")


async def schedule_express_backups(backup_func):
    """Schedule Express backups every 12 hours"""
    while True:
        try:
            await backup_func()
            await asyncio.sleep(12 * 60 * 60)  # 12 hours
        except Exception as e:
            logger.error(f"Express scheduler error: {e}")
            await asyncio.sleep(60 * 60)  # Retry in 1 hour


async def schedule_pro_backups(backup_func):
    """Schedule Pro backups every 24 hours"""
    while True:
        try:
            await backup_func()
            await asyncio.sleep(24 * 60 * 60)  # 24 hours
        except Exception as e:
            logger.error(f"Pro scheduler error: {e}")
            await asyncio.sleep(60 * 60)  # Retry in 1 hour


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS Configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3001"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Audit middleware disabled for WhatsBackup (uses old CRM models)
# from app.core.middleware import AuditMiddleware
# app.add_middleware(AuditMiddleware)



from app.api.v1.endpoints import auth, whatsapp, backups_wa, messages_wa, baileys, plans

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(plans.router, prefix="/api/v1/plans", tags=["plans"])
app.include_router(whatsapp.router, prefix="/api/v1/whatsapp", tags=["whatsapp-pro"])
app.include_router(baileys.router, prefix="/api/v1/baileys", tags=["whatsapp-express"])
app.include_router(backups_wa.router, prefix="/api/v1/backups", tags=["backups"])
app.include_router(messages_wa.router, prefix="/api/v1/messages", tags=["messages"])


@app.get("/health")
def health_check():
    return {"status": "ok", "version": "0.1.0"}

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
