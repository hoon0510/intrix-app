from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from api.db.database import Base

class ExecutionStrategy(Base):
    """
    콘텐츠 실행 전략을 저장하는 테이블
    
    Attributes:
        id: 전략 ID (UUID)
        user_id: 사용자 ID
        analysis_id: 분석 결과 ID
        hook: 훅 메시지 (주목을 끌기 위한 초반부 콘텐츠)
        flow: 플로우 메시지 (중간부 콘텐츠 흐름)
        cta: CTA 메시지 (행동 유도 콜투액션)
        created_at: 생성 시간
    """
    __tablename__ = "execution_strategy"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    analysis_id = Column(String, ForeignKey("analysis_history.id"), index=True)
    hook = Column(Text, nullable=False)
    flow = Column(Text, nullable=False)
    cta = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    user = relationship("User", back_populates="execution_strategies")
    analysis = relationship("AnalysisHistory", back_populates="execution_strategy") 