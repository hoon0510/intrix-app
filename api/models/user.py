from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from api.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    analysis_history = relationship("AnalysisHistory", back_populates="user")
    strategy_history = relationship("StrategyHistory", back_populates="user")
    crawl_history = relationship("CrawlHistory", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")
    execution_strategies = relationship("ExecutionStrategy", back_populates="user") 