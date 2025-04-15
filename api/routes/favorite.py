from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import Dict, List, Optional, Any
from sqlalchemy import desc
import os
import glob
import logging

from api.dependencies.auth import get_current_user_id
from api.db.database import get_db
from api.models.favorite import FavoriteAnalysis
from api.models.history import AnalysisHistory
from pydantic import BaseModel
from api.services.exporter import get_latest_html_file
from api.utils.file_utils import find_latest_pdf_filename, find_latest_html_filename

logger = logging.getLogger(__name__)
router = APIRouter()

class FavoriteResponse(BaseModel):
    id: str
    input_text: str
    result_json: str
    created_at: str

class FavoriteListResponse(BaseModel):
    total_count: int
    items: List[FavoriteResponse]

class FavoriteStatusResponse(BaseModel):
    favorited: bool

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

@router.post("/favorite/{analysis_id}", response_model=Dict[str, str])
async def toggle_favorite(
    analysis_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    분석 결과 즐겨찾기 토글 API
    
    Args:
        analysis_id: 즐겨찾기 대상 분석 ID
        user_id: 현재 로그인한 사용자 ID
        db: 데이터베이스 세션
    
    Returns:
        Dict[str, str]: 토글 결과 상태 ("added" 또는 "removed")
    """
    try:
        # 분석 결과 존재 여부 확인
        analysis = db.query(AnalysisHistory).filter(AnalysisHistory.id == analysis_id).first()
        if not analysis:
            raise HTTPException(status_code=404, detail="분석 결과를 찾을 수 없습니다.")

        # 기존 즐겨찾기 확인
        existing = (
            db.query(FavoriteAnalysis)
            .filter(
                FavoriteAnalysis.user_id == user_id,
                FavoriteAnalysis.analysis_id == analysis_id
            )
            .first()
        )

        if existing:
            # 즐겨찾기 해제
            db.delete(existing)
            db.commit()
            return {"status": "removed"}
        else:
            # 즐겨찾기 추가
            new_fav = FavoriteAnalysis(
                id=str(uuid4()),
                user_id=user_id,
                analysis_id=analysis_id
            )
            db.add(new_fav)
            db.commit()
            return {"status": "added"}
            
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"즐겨찾기 처리 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/favorite", response_model=FavoriteListResponse)
async def get_favorites(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    limit: Optional[int] = 10,
    offset: Optional[int] = 0
):
    """
    즐겨찾기 목록 조회 API
    
    Args:
        user_id: 현재 로그인한 사용자 ID
        db: 데이터베이스 세션
        limit: 페이지당 결과 수
        offset: 시작 위치
    
    Returns:
        FavoriteListResponse: 즐겨찾기 목록과 총 개수
    """
    try:
        # 즐겨찾기 총 개수 조회
        total_count = (
            db.query(FavoriteAnalysis)
            .filter(FavoriteAnalysis.user_id == user_id)
            .count()
        )

        # 즐겨찾기 목록 조회 (페이지네이션 적용)
        favorites = (
            db.query(FavoriteAnalysis)
            .filter(FavoriteAnalysis.user_id == user_id)
            .order_by(desc(FavoriteAnalysis.created_at))
            .offset(offset)
            .limit(limit)
            .all()
        )

        # 분석 결과 ID 목록 추출
        analysis_ids = [f.analysis_id for f in favorites]

        # 분석 결과 조회
        results = (
            db.query(AnalysisHistory)
            .filter(AnalysisHistory.id.in_(analysis_ids))
            .all()
        )

        # 결과 매핑
        results_map = {r.id: r for r in results}

        return FavoriteListResponse(
            total_count=total_count,
            items=[
                FavoriteResponse(
                    id=r.id,
                    input_text=r.input_text,
                    result_json=r.result_json,
                    created_at=r.created_at.isoformat(),
                )
                for r in [results_map[f.analysis_id] for f in favorites]
            ]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"즐겨찾기 목록 조회 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/favorite/status", response_model=FavoriteStatusResponse)
async def check_favorite_status(
    analysis_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    즐겨찾기 상태 확인 API
    
    Args:
        analysis_id: 확인할 분석 ID
        user_id: 현재 로그인한 사용자 ID
        db: 데이터베이스 세션
    
    Returns:
        FavoriteStatusResponse: 즐겨찾기 상태 (true/false)
    """
    try:
        # 분석 결과 존재 여부 확인
        analysis = db.query(AnalysisHistory).filter(AnalysisHistory.id == analysis_id).first()
        if not analysis:
            raise HTTPException(status_code=404, detail="분석 결과를 찾을 수 없습니다.")

        # 즐겨찾기 상태 확인
        exists = (
            db.query(FavoriteAnalysis)
            .filter(
                FavoriteAnalysis.user_id == user_id,
                FavoriteAnalysis.analysis_id == analysis_id
            )
            .first()
        )

        return FavoriteStatusResponse(favorited=bool(exists))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"즐겨찾기 상태 확인 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/favorite")
async def get_favorite_list(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_id)
) -> Dict[str, Any]:
    """
    사용자의 즐겨찾기 목록을 조회합니다.
    """
    try:
        # 전체 레코드 수 조회
        total_count = db.query(FavoriteAnalysis).filter(
            FavoriteAnalysis.user_id == current_user
        ).count()
        
        # 페이지네이션된 레코드 조회
        records = db.query(FavoriteAnalysis).filter(
            FavoriteAnalysis.user_id == current_user
        ).order_by(
            FavoriteAnalysis.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        # 파일명 정보를 포함하여 응답 생성
        items = [
            {
                "id": r.analysis_id,
                "input_text": r.input_text,
                "result_json": r.result_json,
                "created_at": r.created_at.isoformat(),
                "html_filename": find_latest_html_filename(r.analysis_id),
                "pdf_filename": find_latest_pdf_filename(r.analysis_id)
            }
            for r in records
        ]
        
        logger.info(f"즐겨찾기 조회 완료: {len(items)}개 항목")
        return {
            "total_count": total_count,
            "items": items
        }
        
    except Exception as e:
        logger.error(f"즐겨찾기 조회 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"즐겨찾기 조회 중 오류가 발생했습니다: {str(e)}"
        ) 