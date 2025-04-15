from sqlalchemy import Column, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from api.db.database import Base

class FavoriteAnalysis(Base):
    """분석 결과 즐겨찾기 모델"""
    __tablename__ = "favorite_analysis"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    analysis_id = Column(String, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 사용자별 분석 결과 중복 등록 방지
    __table_args__ = (
        UniqueConstraint("user_id", "analysis_id", name="user_analysis_unique"),
    ) 