"""
Credits Endpoint Router
"""

from fastapi import APIRouter, HTTPException
from typing import List
from ..services.credit_manager import CreditManager

router = APIRouter(prefix="/credits", tags=["credits"])
credit_manager = CreditManager()

@router.get("/balance/{user_id}")
async def get_credit_balance(user_id: str):
    """
    Get user's credit balance
    """
    try:
        # Replace None with actual DB connection
        balance = None  # Implement actual DB query
        return {"user_id": user_id, "balance": balance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/calculate")
async def calculate_required_credits(
    text_size: int,
    community_channels: List[str],
    sns_channels: List[str]
):
    """
    Calculate required credits for a request
    """
    try:
        credits = credit_manager.calculate_total_credits(
            text_size,
            community_channels,
            sns_channels
        )
        return {"required_credits": credits}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 