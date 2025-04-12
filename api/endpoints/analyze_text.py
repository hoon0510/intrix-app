# 📁 api/endpoints/analyze_text.py

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from api.services.claude_service import analyze_emotion
from api.services.gpt_service import generate_strategy, generate_copy, generate_performance
from api.services.formatter import format_report

router = APIRouter()

class AnalyzeTextRequest(BaseModel):
    user_id: str
    uuid: str  # 세션 고유 ID
    input_text: str

@router.post("/analyze/text")
async def analyze_text(payload: AnalyzeTextRequest):
    try:
        # Step 1. 감정/욕구 분석 (Claude)
        analysis_result = await analyze_emotion(payload.input_text)

        # Step 2. 전략 설계 (GPT)
        strategy_result = await generate_strategy(analysis_result)

        # Step 3. 카피라이팅 (GPT)
        copy_result = await generate_copy(analysis_result)

        # Step 4. 퍼포먼스 설계 (GPT)
        performance_result = await generate_performance(analysis_result)

        # Step 5. Claude 포맷팅 (HTML)
        formatted_html = await format_report(
            strategy=strategy_result,
            copy=copy_result,
            performance=performance_result,
            analysis=analysis_result
        )

        return {
            "status": "success",
            "uuid": payload.uuid,
            "html": formatted_html
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 실패: {str(e)}")
