from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid
from datetime import datetime

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    plan_type = Column(String, nullable=False)  # 'express' or 'pro'
    status = Column(String, default="active")  # 'active', 'cancelled', 'past_due'
    
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)
    cancel_at_period_end = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Payment tracking (Stripe integration)
    stripe_subscription_id = Column(String, nullable=True)
    stripe_customer_id = Column(String, nullable=True)
    price_monthly = Column(Numeric(10, 2), nullable=True)
    
    # Usage tracking (for Express plan limits)
    messages_this_period = Column(Integer, default=0)
    max_messages = Column(Integer, default=5000)  # 5K for Express
    
    # Relationships
    user = relationship("User", backref="subscriptions")
    
    def __repr__(self):
        return f"<Subscription {self.id} - {self.plan_type} - {self.status}>"
