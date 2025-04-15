from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional, Dict, Any
from uuid import uuid4
import json
import os
import glob
import logging

from api.dependencies.auth import get_current_user_id
from api.db.database import get_db
from api.models.history import AnalysisHistory, StrategyHistory, CrawlHistory, History
from pydantic import BaseModel
from api.utils.auth import get_current_user
from api.services.exporter import get_latest_html_file
from api.utils.file_utils import find_latest_pdf_filename, find_latest_html_filename

logger = logging.getLogger(__name__)
router = APIRouter()

# 요청/응답 모델
class HistorySaveRequest(BaseModel):
    input_text: str
    result_json: str

class StrategySaveRequest(BaseModel):
    analysis_id: str
    strategy_type: str
    result_json: str

class CrawlSaveRequest(BaseModel):
    input_text: str
    channels: List[str]
    result_count: int
    result_json: str

class HistoryResponse(BaseModel):
    id: str
    input_text: str
    result_json: str
    created_at: str

class HistoryListResponse(BaseModel):
    total_count: int
    items: List[HistoryResponse]

def find_latest_pdf_filename(analysis_id: str) -> Optional[str]:
    """
    주어진 분석 ID에 대한 가장 최근 PDF 파일명을 찾습니다.
    
    Args:
        analysis_id (str): 분석 ID
        
    Returns:
        Optional[str]: 가장 최근 PDF 파일명 또는 None
    """
    try:
        files = glob.glob(f"exported_pdfs/{analysis_id}_*.pdf")
        if not files:
            return None
        return os.path.basename(max(files, key=os.path.getctime))
    except Exception as e:
        print(f"PDF 파일명 검색 중 오류: {str(e)}")
        return None

# 분석 결과 저장
@router.post("/analysis")
async def save_analysis_history(
    data: HistorySaveRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    try:
        record = AnalysisHistory(
            id=str(uuid4()),
            user_id=user_id,
            input_text=data.input_text,
            result_json=data.result_json,
        )
        db.add(record)
        db.commit()
        return {"status": "ok", "id": record.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 전략 결과 저장
@router.post("/strategy")
async def save_strategy_history(
    data: StrategySaveRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    try:
        record = StrategyHistory(
            id=str(uuid4()),
            analysis_id=data.analysis_id,
            user_id=user_id,
            strategy_type=data.strategy_type,
            result_json=data.result_json,
        )
        db.add(record)
        db.commit()
        return {"status": "ok", "id": record.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 크롤링 결과 저장
@router.post("/crawl")
async def save_crawl_history(
    data: CrawlSaveRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    try:
        record = CrawlHistory(
            id=str(uuid4()),
            user_id=user_id,
            input_text=data.input_text,
            channels=json.dumps(data.channels),
            result_count=data.result_count,
            result_json=data.result_json,
        )
        db.add(record)
        db.commit()
        return {"status": "ok", "id": record.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 분석 이력 조회
@router.get("/analysis", response_model=List[HistoryResponse])
async def get_analysis_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        # 총 결과 수 조회
        total_count = (
            db.query(func.count(AnalysisHistory.id))
            .filter(AnalysisHistory.user_id == current_user["id"])
            .scalar()
        )

        # 페이지네이션 적용하여 결과 조회
        records = (
            db.query(AnalysisHistory)
            .filter(AnalysisHistory.user_id == current_user["id"])
            .order_by(AnalysisHistory.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        # 각 기록에 대해 PDF 파일명 추가
        for record in records:
            record.pdf_filename = find_latest_pdf_filename(record.id)
        
        return HistoryListResponse(
            total_count=total_count,
            items=[
                HistoryResponse(
                    id=r.id,
                    input_text=r.input_text,
                    result_json=r.result_json,
                    created_at=r.created_at.isoformat(),
                )
                for r in records
            ]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"분석 이력 조회 중 오류가 발생했습니다: {str(e)}"
        )

# 전략 이력 조회
@router.get("/strategy", response_model=List[HistoryResponse])
async def get_strategy_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    records = db.query(StrategyHistory)\
        .filter(StrategyHistory.user_id == current_user["id"])\
        .order_by(StrategyHistory.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return [
        HistoryResponse(
            id=record.id,
            input_text=f"전략 유형: {record.strategy_type}",
            result_json=record.result_json,
            created_at=record.created_at.isoformat(),
        )
        for record in records
    ]

# 크롤링 이력 조회
@router.get("/crawl", response_model=List[HistoryResponse])
async def get_crawl_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    records = db.query(CrawlHistory)\
        .filter(CrawlHistory.user_id == current_user["id"])\
        .order_by(CrawlHistory.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return [
        HistoryResponse(
            id=record.id,
            input_text=f"{record.input_text} ({json.loads(record.channels)})",
            result_json=record.result_json,
            created_at=record.created_at.isoformat(),
        )
        for record in records
    ]

@router.get("/history")
async def get_history_list(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    사용자의 분석 이력을 조회합니다.
    """
    try:
        # 전체 레코드 수 조회
        total_count = db.query(History).filter(
            History.user_id == current_user.id
        ).count()
        
        # 페이지네이션된 레코드 조회
        records = db.query(History).filter(
            History.user_id == current_user.id
        ).order_by(
            History.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        # 파일명 정보를 포함하여 응답 생성
        items = [
            {
                "id": r.id,
                "input_text": r.input_text,
                "result_json": r.result_json,
                "created_at": r.created_at.isoformat(),
                "html_filename": find_latest_html_filename(r.id),
                "pdf_filename": find_latest_pdf_filename(r.id)
            }
            for r in records
        ]
        
        logger.info(f"이력 조회 완료: {len(items)}개 항목")
        return {
            "total_count": total_count,
            "items": items
        }
        
    except Exception as e:
        logger.error(f"이력 조회 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"이력 조회 중 오류가 발생했습니다: {str(e)}"
        ) 