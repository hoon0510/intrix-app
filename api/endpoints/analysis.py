"""
Analysis Endpoint Router
"""

from fastapi import APIRouter, HTTPException
from typing import List
from ..services.analyzer_claude import Analyzer
from ..services.credit_manager import CreditManager

router = APIRouter(prefix="/analysis", tags=["analysis"])
analyzer = Analyzer()
credit_manager = CreditManager()

@router.post("/text")
async def analyze_text(text: str, user_id: str):
    """
    Analyze a single text
    """
    try:
        # Calculate required credits
        text_size = len(text.encode('utf-8'))
        required_credits = credit_manager.calculate_base_credits(text_size)
        
        # Check and deduct credits
        if not credit_manager.check_credits(user_id, required_credits, None):  # Replace None with actual DB connection
            raise HTTPException(status_code=402, detail="Insufficient credits")
            
        # Perform analysis
        result = analyzer.analyze_text(text)
        
        # Deduct credits
        credit_manager.deduct_credits(user_id, required_credits, None)  # Replace None with actual DB connection
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/texts")
async def analyze_multiple_texts(texts: List[str], user_id: str):
    """
    Analyze multiple texts
    """
    try:
        # Calculate required credits
        total_size = sum(len(text.encode('utf-8')) for text in texts)
        required_credits = credit_manager.calculate_base_credits(total_size)
        
        # Check and deduct credits
        if not credit_manager.check_credits(user_id, required_credits, None):  # Replace None with actual DB connection
            raise HTTPException(status_code=402, detail="Insufficient credits")
            
        # Perform analysis
        result = analyzer.analyze_multiple_texts(texts)
        
        # Deduct credits
        credit_manager.deduct_credits(user_id, required_credits, None)  # Replace None with actual DB connection
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 