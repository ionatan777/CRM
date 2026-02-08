"""
Pro Plan Backup Scheduler
Runs every 24 hours for users on Pro plan
"""

import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.integrations.whatsapp_api import WhatsAppAPIService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_pro_backup():
    """Run backup for all Pro plan users"""
    logger.info("🔄 Starting Pro plan auto-backup...")
    
    db = SessionLocal()
    
    try:
        # Get all Pro users with auto-backup enabled
        users = db.query(User).filter(
            User.plan_type == 'pro',
            User.auto_backup_enabled == True,
            User.whatsapp_phone_id.isnot(None),
            User.whatsapp_access_token.isnot(None)
        ).all()
        
        logger.info(f"Found {len(users)} Pro users for backup")
        
        for user in users:
            try:
                logger.info(f"Backing up user {user.email}...")
                
                service = WhatsAppAPIService(
                    user.whatsapp_phone_id,
                    user.whatsapp_access_token
                )
                
                result = await service.create_backup(user.id, db)
                logger.info(f"✅ Backup completed: {result['total_messages']} messages")
                
            except Exception as e:
                logger.error(f"❌ Backup failed for {user.email}: {e}")
                continue
        
        logger.info("✅ Pro auto-backup completed")
        
    except Exception as e:
        logger.error(f"Pro backup scheduler error: {e}")
    finally:
        db.close()

async def scheduler_loop():
    """Main scheduler - runs every 24 hours at 3 AM"""
    logger.info("🚀 Pro Backup Scheduler Started (every 24 hours)")
    
    while True:
        try:
            await run_pro_backup()
            logger.info("⏰ Next Pro backup in 24 hours...")
            await asyncio.sleep(24 * 60 * 60)  # 24 hours
            
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
            await asyncio.sleep(60 * 60)  # Retry in 1 hour

if __name__ == "__main__":
    asyncio.run(scheduler_loop())
