# Auto-backup scheduler for WhatsBackup
# This runs as a background task to automatically backup WhatsApp conversations

import asyncio
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.services.whatsapp_backup import WhatsAppBackupService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_auto_backup_for_user(user: User, db: Session):
    """Run backup for a single user"""
    try:
        logger.info(f"Starting auto-backup for user: {user.email}")
        
        service = WhatsAppBackupService(
            user.whatsapp_phone_id,
            user.whatsapp_access_token
        )
        
        result = await service.create_backup(user.id, db)
        
        logger.info(
            f"✅ Backup completed for {user.email}: "
            f"{result['total_messages']} messages, "
            f"{result['total_contacts']} contacts"
        )
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Backup failed for {user.email}: {e}")
        return None

async def auto_backup_all_users():
    """
    Auto-backup task that runs periodically
    Backs up all users who have:
    - auto_backup_enabled = True
    - WhatsApp connected (phone_id and access_token set)
    """
    
    logger.info("🔄 Starting auto-backup scheduler...")
    
    db = SessionLocal()
    
    try:
        # Get all users eligible for auto-backup
        users = db.query(User).filter(
            User.auto_backup_enabled == True,
            User.whatsapp_phone_id.isnot(None),
            User.whatsapp_access_token.isnot(None)
        ).all()
        
        logger.info(f"Found {len(users)} users for auto-backup")
        
        if len(users) == 0:
            logger.info("No users to backup. Exiting.")
            return
        
        # Run backups concurrently
        tasks = [run_auto_backup_for_user(user, db) for user in users]
        results = await asyncio.gather(*tasks)
        
        # Summary
        successful = sum(1 for r in results if r is not None)
        failed = len(results) - successful
        
        logger.info(f"\n📊 Auto-backup Summary:")
        logger.info(f"   ✅ Successful: {successful}")
        logger.info(f"   ❌ Failed: {failed}")
        
    except Exception as e:
        logger.error(f"Auto-backup scheduler error: {e}")
    finally:
        db.close()

async def scheduler_loop():
    """
    Main scheduler loop - runs auto-backup every 24 hours
    """
    
    logger.info("🚀 WhatsBackup Auto-Scheduler Started")
    logger.info("📅 Running backups every 24 hours")
    
    while True:
        try:
            await auto_backup_all_users()
            
            # Wait 24 hours
            logger.info(f"⏰ Next backup scheduled in 24 hours...")
            await asyncio.sleep(24 * 60 * 60)  # 24 hours
            
        except Exception as e:
            logger.error(f"Scheduler loop error: {e}")
            # Wait 1 hour before retrying on error
            await asyncio.sleep(60 * 60)

if __name__ == "__main__":
    # Run the scheduler
    asyncio.run(scheduler_loop())
