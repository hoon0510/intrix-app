from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from api.db.database import get_db
from api.models.admin_log import AnalysisLog
from api.dependencies.auth import get_current_user_id

router = APIRouter()

@router.get("/mypage/credit-log")
async def get_user_credit_log(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
) -> List[dict]:
    """
    사용자의 크레딧 사용 이력을 조회합니다.
    
    Args:
        db: 데이터베이스 세션
        user_id: 현재 사용자 ID
        
    Returns:
        List[dict]: 크레딧 사용 이력 목록
            - analysis_type: 분석 유형
            - input_text: 입력 텍스트 (100자 제한)
            - credit_used: 사용된 크레딧
            - created_at: 생성 시간 (ISO 형식)
            
    Raises:
        HTTPException: 데이터 조회 실패 시
    """
    try:
        # 사용자의 크레딧 사용 이력 조회
        logs = (
            db.query(AnalysisLog)
            .filter(AnalysisLog.user_id == user_id)
            .order_by(AnalysisLog.created_at.desc())
            .all()
        )
        
        # 결과 포맷팅
        return [
            {
                "analysis_type": log.analysis_type,
                "input_text": log.input_text[:100] + "..." if len(log.input_text) > 100 else log.input_text,
                "credit_used": log.credit_used,
                "created_at": log.created_at.isoformat()
            }
            for log in logs
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"크레딧 사용 이력 조회 중 오류가 발생했습니다: {str(e)}"
        ) 