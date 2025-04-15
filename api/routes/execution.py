from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
import logging
from typing import Optional
from api.dependencies.auth import get_current_user_id
from api.db.database import get_db
from api.models.execution import ExecutionStrategy
from pydantic import BaseModel
from api.services.gpt_executor import generate_execution_strategy
from api.services.logger import log_analysis
from datetime import datetime
import time

# 로거 설정
logger = logging.getLogger(__name__)

router = APIRouter()

class ExecutionRequest(BaseModel):
    analysis_id: str
    input_text: str  # Claude로 분석된 핵심 욕구 요약 텍스트

class ExecutionResponse(BaseModel):
    status: str
    id: str
    hook: str
    flow: str
    cta: str
    created_at: datetime

@router.post("/execution", response_model=ExecutionResponse)
async def create_execution_strategy(
    data: ExecutionRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    분석 결과를 기반으로 콘텐츠 실행 전략을 생성하고 저장합니다.
    
    Args:
        data: 분석 ID와 입력 텍스트를 포함한 요청 데이터
        user_id: 현재 사용자 ID
        db: 데이터베이스 세션
        
    Returns:
        ExecutionResponse: 생성된 실행 전략 정보
        
    Raises:
        HTTPException: 전략 생성 실패 시
    """
    try:
        logger.info(f"Starting execution strategy generation for analysis_id: {data.analysis_id}")
        
        # 실행 전략 생성 시작 시간 기록
        start_time = time.time()
        
        # 기존 전략이 있는지 확인
        existing_strategy = db.query(ExecutionStrategy).filter(
            ExecutionStrategy.analysis_id == data.analysis_id
        ).first()
        
        # GPT를 통해 실행 전략 생성
        hook, flow, cta = await generate_execution_strategy(data.input_text)
        logger.info("Execution strategy generated successfully")
        
        if existing_strategy:
            # 기존 전략 업데이트
            existing_strategy.hook = hook
            existing_strategy.flow = flow
            existing_strategy.cta = cta
            strategy_id = existing_strategy.id
            logger.info(f"Updated existing strategy: {strategy_id}")
        else:
            # 새 전략 생성
            strategy_id = str(uuid4())
            record = ExecutionStrategy(
                id=strategy_id,
                user_id=user_id,
                analysis_id=data.analysis_id,
                hook=hook,
                flow=flow,
                cta=cta
            )
            db.add(record)
            logger.info(f"Created new strategy: {strategy_id}")
        
        db.commit()
        
        # 처리 시간 계산
        processing_time = time.time() - start_time
        
        # 분석 로그 기록
        log_analysis(
            db=db,
            user_id=user_id,
            analysis_type="실행전략",
            input_text=data.input_text,
            credit_used=1,  # 실행 전략 생성에 필요한 크레딧
            processing_time=processing_time
        )
        
        return ExecutionResponse(
            status="ok",
            id=strategy_id,
            hook=hook,
            flow=flow,
            cta=cta,
            created_at=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error generating execution strategy: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate execution strategy: {str(e)}"
        )

@router.get("/execution/{analysis_id}", response_model=ExecutionResponse)
async def get_execution_strategy(
    analysis_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    특정 분석에 대한 실행 전략을 조회합니다.
    
    Args:
        analysis_id: 분석 ID
        user_id: 현재 사용자 ID
        db: 데이터베이스 세션
        
    Returns:
        ExecutionResponse: 실행 전략 정보
        
    Raises:
        HTTPException: 전략이 존재하지 않거나 권한이 없는 경우
    """
    try:
        logger.info(f"Retrieving execution strategy for analysis_id: {analysis_id}")
        
        # 실행 전략 조회
        strategy = db.query(ExecutionStrategy).filter(
            ExecutionStrategy.analysis_id == analysis_id,
            ExecutionStrategy.user_id == user_id
        ).first()
        
        if not strategy:
            logger.warning(f"Execution strategy not found for analysis_id: {analysis_id}")
            raise HTTPException(
                status_code=404,
                detail="실행 전략이 존재하지 않습니다."
            )
            
        logger.info(f"Successfully retrieved execution strategy: {strategy.id}")
        return ExecutionResponse(
            status="ok",
            id=strategy.id,
            hook=strategy.hook,
            flow=strategy.flow,
            cta=strategy.cta,
            created_at=strategy.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving execution strategy: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"실행 전략 조회 중 오류가 발생했습니다: {str(e)}"
        ) 