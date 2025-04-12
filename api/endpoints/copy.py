"""
Copy Endpoint Router
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Optional
from ..services.copywriter import Copywriter
from ..services.credit_manager import CreditManager

router = APIRouter(prefix="/copy", tags=["copy"])
copywriter = Copywriter()
credit_manager = CreditManager()

@router.post("/generate")
async def generate_copy(
    strategy: Dict,
    analysis_result: Dict,
    user_id: str,
    style: Optional[str] = None
):
    """
    Generate marketing copy based on strategy and analysis
    """
    try:
        # Calculate required credits (copy generation uses fixed credits)
        required_credits = 5  # Example fixed credit cost
        
        # Check and deduct credits
        if not credit_manager.check_credits(user_id, required_credits, None):  # Replace None with actual DB connection
            raise HTTPException(status_code=402, detail="Insufficient credits")
            
        # Generate copy
        result = copywriter.generate_copy(strategy, analysis_result, style)
        
        # Deduct credits
        credit_manager.deduct_credits(user_id, required_credits, None)  # Replace None with actual DB connection
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 