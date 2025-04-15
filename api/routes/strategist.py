from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from pydantic import BaseModel
import time
import logging
from api.database import get_db
from api.utils.auth import get_current_user_id
from api.services.claude import claude_strategy_function
from api.services.logger import log_analysis
from api.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()

class StrategyRequest(BaseModel):
    input_text: str
    analysis_id: Optional[str] = None

class StrategyResponse(BaseModel):
    result_json: Dict
    credit_used: int

@router.post("/strategist", response_model=StrategyResponse)
async def generate_strategy(
    data: StrategyRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> StrategyResponse:
    """
    전략 분석을 생성합니다.
    """
    try:
        # 사용자 정보 조회
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
            
        # 크레딧 확인
        estimated_credit = 10  # 전략 생성에 필요한 크레딧
        if user.credits < estimated_credit:
            raise HTTPException(
                status_code=400,
                detail="크레딧이 부족합니다."
            )
            
        # 전략 생성 시작 시간 기록
        start_time = time.time()
        
        # Claude API 호출
        result = claude_strategy_function(data.input_text)
        
        # 처리 시간 계산
        processing_time = time.time() - start_time
        
        # 크레딧 차감
        user.credits -= estimated_credit
        db.commit()
        
        # 분석 로그 기록
        log_analysis(
            db=db,
            user_id=user_id,
            analysis_type="전략",
            input_text=data.input_text,
            credit_used=estimated_credit,
            processing_time=processing_time
        )
        
        logger.info(f"전략 생성 완료 - 사용자: {user_id}, 크레딧 사용: {estimated_credit}")
        
        return StrategyResponse(
            result_json=result,
            credit_used=estimated_credit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"전략 생성 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"전략 생성 중 오류가 발생했습니다: {str(e)}"
        ) 