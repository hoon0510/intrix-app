from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from api.db.database import Base
import uuid

class AnalysisHistory(Base):
    """
    분석 결과를 저장하는 테이블
    """
    __tablename__ = "analysis_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), index=True, nullable=False)
    input_text = Column(Text, nullable=False)
    result_json = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 관계 설정
    strategies = relationship("StrategyHistory", back_populates="analysis")

class StrategyHistory(Base):
    """
    전략 생성 결과를 저장하는 테이블
    """
    __tablename__ = "strategy_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id = Column(String(36), ForeignKey("analysis_history.id"), nullable=False)
    user_id = Column(String(36), index=True, nullable=False)
    strategy_type = Column(String(50), nullable=False)  # "existing" or "new"
    result_json = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 관계 설정
    analysis = relationship("AnalysisHistory", back_populates="strategies")

class CrawlHistory(Base):
    """
    크롤링 결과를 저장하는 테이블
    """
    __tablename__ = "crawl_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), index=True, nullable=False)
    input_text = Column(Text, nullable=False)
    channels = Column(Text, nullable=False)  # JSON string of channel list
    result_count = Column(Integer, nullable=False)
    result_json = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 