from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from datetime import datetime, timedelta
from api.db.database import get_db
from api.models.admin_log import AnalysisLog
from api.dependencies.auth import get_current_user_id

router = APIRouter()

@router.get("/admin/stats")
async def get_admin_stats(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
) -> Dict[str, Any]:
    """
    관리자 대시보드용 통계 데이터를 반환합니다.
    
    Returns:
        Dict[str, Any]: 통계 데이터
            - total_requests: 전체 요청 수
            - total_credits: 누적 크레딧 사용량
            - recent_activity: 최근 7일간의 일자별 요청 수
    """
    try:
        # 전체 요청 수 조회
        total_requests = db.query(func.count(AnalysisLog.id)).scalar()
        
        # 누적 크레딧 사용량 조회
        total_credits = db.query(func.coalesce(func.sum(AnalysisLog.credit_used), 0)).scalar()
        
        # 최근 7일간의 일자별 요청 수 조회
        recent_days = (
            db.query(
                func.date_trunc("day", AnalysisLog.created_at).label("day"),
                func.count().label("count")
            )
            .group_by("day")
            .order_by("day desc")
            .limit(7)
            .all()
        )
        
        # 결과 포맷팅
        recent_activity = [
            {
                "date": str(row.day.date()),
                "count": row.count
            }
            for row in recent_days
        ]
        
        return {
            "total_requests": total_requests,
            "total_credits": total_credits,
            "recent_activity": recent_activity
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"통계 데이터 조회 중 오류가 발생했습니다: {str(e)}"
        ) 