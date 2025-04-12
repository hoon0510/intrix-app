"""
Strategy Endpoint Router
"""

from fastapi import APIRouter, HTTPException
from typing import Dict
from ..services.strategist import Strategist
from ..services.credit_manager import CreditManager

router = APIRouter(prefix="/strategy", tags=["strategy"])
strategist = Strategist()
credit_manager = CreditManager()

@router.post("/generate")
async def generate_strategy(analysis_result: Dict, user_id: str, prompt_type: str = "existing"):
    """
    Generate marketing strategy based on analysis results
    """
    try:
        # Calculate required credits (strategy generation uses fixed credits)
        required_credits = 10  # Example fixed credit cost
        
        # Check and deduct credits
        if not credit_manager.check_credits(user_id, required_credits, None):  # Replace None with actual DB connection
            raise HTTPException(status_code=402, detail="Insufficient credits")
            
        # Generate strategy
        result = strategist.generate_strategy(analysis_result, prompt_type)
        
        # Deduct credits
        credit_manager.deduct_credits(user_id, required_credits, None)  # Replace None with actual DB connection
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 