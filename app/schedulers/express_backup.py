"""
Express Plan Backup Scheduler
Runs every 12 hours for users on Express plan
"""

import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.integrations.whatsapp_baileys import BaileysService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

baileys_service = BaileysService()

async def run_express_backup():
    """Run backup for all Express plan users"""
    logger.info("🔄 Starting Express plan auto-backup...")
    
    db = SessionLocal()
    
    try:
        # Get all Express users with auto-backup enabled
        users = db.query(User).filter(
            User.plan_type == 'express',
            User.auto_backup_enabled == True,
            User.baileys_session_id.isnot(None)
        ).all()
        
        logger.info(f"Found {len(users)} Express users for backup")
        
        for user in users:
            try:
                logger.info(f"Backing up user {user.email}...")
                result = await baileys_service.create_backup(user.id, db)
                logger.info(f"✅ Backup completed: {result['total_messages']} messages")
                
            except Exception as e:
                logger.error(f"❌ Backup failed for {user.email}: {e}")
                continue
        
        logger.info("✅ Express auto-backup completed")
        
    except Exception as e:
        logger.error(f"Express backup scheduler error: {e}")
    finally:
        db.close()

async def scheduler_loop():
    """Main scheduler - runs every 12 hours"""
    logger.info("🚀 Express Backup Scheduler Started (every 12 hours)")
    
    while True:
        try:
            await run_express_backup()
            logger.info("⏰ Next Express backup in 12 hours...")
            await asyncio.sleep(12 * 60 * 60)  # 12 hours
            
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
            await asyncio.sleep(60 * 60)  # Retry in 1 hour

if __name__ == "__main__":
    asyncio.run(scheduler_loop())
