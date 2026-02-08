"""
Plans API Endpoints
Allows users to select and manage their subscription plans
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.plans import get_plan_limits, PLANS, upgrade_to_pro
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()


class PlanInfo(BaseModel):
    """Plan information model"""
    plan_type: str
    price: float
    max_messages: int = None
    backup_frequency_hours: int
    features: List[str]


class SelectPlanRequest(BaseModel):
    """Request to select a plan"""
    plan_type: str  # 'express' or 'pro'


@router.get("/list")
def list_plans() -> List[PlanInfo]:
    """
    Get list of all available plans
    """
    plans_list = []
    
    for plan_type, details in PLANS.items():
        plans_list.append(PlanInfo(
            plan_type=plan_type,
            price=details['price'],
            max_messages=details['max_messages'],
            backup_frequency_hours=details['backup_frequency_hours'],
            features=details['features']
        ))
    
    return plans_list


@router.post("/select")
def select_plan(
    request: SelectPlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Select a plan for the current user
    """
    if request.plan_type not in ['express', 'pro']:
        raise HTTPException(status_code=400, detail="Invalid plan type")
    
    # Update user's plan
    current_user.plan_type = request.plan_type
    current_user.plan_status = 'trial'  # Start with trial
    
    # Set backup frequency based on plan
    if request.plan_type == 'express':
        current_user.backup_frequency_hours = 12
    else:
        current_user.backup_frequency_hours = 24
    
    db.commit()
    
    return {
        "message": f"Successfully selected {request.plan_type.capitalize()} plan",
        "plan_type": request.plan_type,
        "status": "trial"
    }


@router.post("/upgrade-to-pro")
def upgrade_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upgrade from Express to Pro plan
    """
    if current_user.plan_type == 'pro':
        raise HTTPException(status_code=400, detail="Already on Pro plan")
    
    success = upgrade_to_pro(current_user.id, db)
    
    if success:
        return {
            "message": "Successfully upgraded to Pro plan",
            "plan_type": "pro",
            "status": "active"
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to upgrade plan")


@router.get("/current")
def get_current_plan(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get current user's plan information
    """
    plan_limits = get_plan_limits(current_user.plan_type or 'express')
    
    return {
        "plan_type": current_user.plan_type,
        "plan_status": current_user.plan_status,
        "backup_frequency_hours": current_user.backup_frequency_hours,
        "limits": plan_limits
    }
