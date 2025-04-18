from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services.ai_service import ai_service

router = APIRouter()

class AnalysisRequest(BaseModel):
    text: str
    analysis_type: str  # "new", "retention", "desire", "report"

class AnalysisResponse(BaseModel):
    success: bool
    message: str
    analysis: Optional[dict] = None

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(request: AnalysisRequest):
    try:
        # GPT로 분석 시도, 실패하면 자동으로 Claude로 폴백
        analysis_result = await ai_service.analyze_with_gpt(
            text=request.text,
            analysis_type=request.analysis_type
        )
        
        return AnalysisResponse(
            success=True,
            message="분석이 완료되었습니다.",
            analysis=analysis_result
        )

    except Exception as e:
        print(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 