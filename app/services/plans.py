"""
Plan Management Service
Handles plan limits, upgrades, and usage tracking for Express and Pro plans
"""

from sqlalchemy.orm import Session
from app.models.user import User
from app.models.subscription import Subscription
from typing import Dict, Tuple
from uuid import UUID
from datetime import datetime

# Plan Configuration
PLANS = {
    'express': {
        'price': 18.00,  # $18/month
        'max_messages': 5000,
        'backup_frequency_hours': 12,
        'features': [
            'Connection via QR (Baileys)',
            'Automatic backups every 12 hours',
            'Up to 5,000 messages/month',
            'Message search',
            'PDF export',
        ]
    },
    'pro': {
        'price': 35.00,  # $35/month
        'max_messages': None,  # Unlimited
        'backup_frequency_hours': 24,
        'features': [
            'WhatsApp Business API connection',
            'Automatic backups every 24 hours',
            'Unlimited messages',
            'Message search',
            'PDF export',
            'Multi-device support',
            'Business analytics (coming soon)',
        ]
    }
}


def check_plan_type(user_id: UUID, db: Session) -> str:
    """
    Returns the current plan type for a user
    Returns: 'express' or 'pro'
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    
    return user.plan_type or 'express'


def can_create_backup(user_id: UUID, db: Session) -> Tuple[bool, str]:
    """
    Check if user can create a backup based on their plan limits
    
    Returns:
        (can_backup: bool, reason: str)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False, "User not found"
    
    plan_type = user.plan_type or 'express'
    
    # Pro plan has unlimited backups
    if plan_type == 'pro':
        return True, "Pro plan - unlimited backups"
    
    # Express plan - check message limit
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.status == 'active'
    ).first()
    
    if not subscription:
        return False, "No active subscription found"
    
    if subscription.messages_this_period >= subscription.max_messages:
        return False, f"Message limit reached ({subscription.max_messages} messages). Upgrade to Pro for unlimited messages."
    
    return True, "Within message limit"


def get_plan_limits(plan_type: str) -> Dict:
    """
    Get the limits and features for a specific plan
    
    Args:
        plan_type: 'express' or 'pro'
    
    Returns:
        Dictionary with plan details
    """
    if plan_type not in PLANS:
        raise ValueError(f"Invalid plan type: {plan_type}")
    
    return PLANS[plan_type]


def increment_message_count(user_id: UUID, count: int, db: Session) -> None:
    """
    Increment the message count for the current billing period (Express plan only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return
    
    # Only track for Express plan
    if user.plan_type == 'express':
        subscription = db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.status == 'active'
        ).first()
        
        if subscription:
            subscription.messages_this_period += count
            db.commit()


def check_message_limit(user_id: UUID, db: Session) -> Tuple[bool, int]:
    """
    Check if user has hit their message limit
    
    Returns:
        (is_over_limit: bool, messages_remaining: int)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return True, 0
    
    # Pro plan has no message limit
    if user.plan_type == 'pro':
        return False, -1  # -1 indicates unlimited
    
    # Express plan
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.status == 'active'
    ).first()
    
    if not subscription:
        return True, 0
    
    messages_used = subscription.messages_this_period
    max_messages = subscription.max_messages
    messages_remaining = max(0, max_messages - messages_used)
    
    is_over_limit = messages_used >= max_messages
    
    return is_over_limit, messages_remaining


def upgrade_to_pro(user_id: UUID, db: Session) -> bool:
    """
    Upgrade a user from Express to Pro plan
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    
    # Update user plan
    user.plan_type = 'pro'
    user.backup_frequency_hours = 24  # Pro backups every 24h
    
    # Cancel old Express subscription
    old_subscription = db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.plan_type == 'express',
        Subscription.status == 'active'
    ).first()
    
    if old_subscription:
        old_subscription.status = 'cancelled'
        old_subscription.cancel_at_period_end = True
    
    # Create new Pro subscription
    new_subscription = Subscription(
        user_id=user_id,
        plan_type='pro',
        status='active',
        price_monthly=PLANS['pro']['price'],
        max_messages=None,  # Unlimited
        current_period_start=datetime.utcnow()
    )
    db.add(new_subscription)
    db.commit()
    
    return True
