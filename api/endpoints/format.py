"""
Format Endpoint Router
"""

from fastapi import APIRouter, HTTPException
from typing import Dict
from ..services.formatter_claude import Formatter
from ..services.credit_manager import CreditManager

router = APIRouter(prefix="/format", tags=["format"])
formatter = Formatter()
credit_manager = CreditManager()

@router.post("/report")
async def format_report(
    strategy: Dict,
    analysis: Dict,
    copy: Dict,
    user_id: str,
    output_format: str = "html"
):
    """
    Format the final report
    """
    try:
        # Calculate required credits (formatting uses fixed credits)
        required_credits = 3  # Example fixed credit cost
        
        # Check and deduct credits
        if not credit_manager.check_credits(user_id, required_credits, None):  # Replace None with actual DB connection
            raise HTTPException(status_code=402, detail="Insufficient credits")
            
        # Format report
        result = formatter.format_report(strategy, analysis, copy)
        
        # Generate output in requested format
        if output_format == "html":
            output = formatter.generate_html(result)
        else:
            output = result  # Return JSON by default
            
        # Deduct credits
        credit_manager.deduct_credits(user_id, required_credits, None)  # Replace None with actual DB connection
        
        return {"format": output_format, "content": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 