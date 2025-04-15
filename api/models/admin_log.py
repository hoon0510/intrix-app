from sqlalchemy import Column, String, DateTime, Integer, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from api.db.database import Base

class AnalysisLog(Base):
    """
    분석 요청 로그를 기록하는 테이블
    
    Attributes:
        id (str): 로그 ID (UUID)
        user_id (str): 사용자 ID
        input_text (str): 입력 텍스트
        analysis_type (str): 분석 유형 (전략/카피/실행전략)
        credit_used (int): 사용된 크레딧
        processing_time (float): 처리 시간(초)
        created_at (datetime): 생성 시간
    """
    __tablename__ = "analysis_log"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    input_text = Column(String)
    analysis_type = Column(String)  # '전략', '카피', '실행전략'
    credit_used = Column(Integer)
    processing_time = Column(Float)  # 처리 시간(초)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    user = relationship("User", back_populates="analysis_logs")

class UserCreditLog(Base):
    """
    사용자 크레딧 변동 로그를 기록하는 테이블
    
    Attributes:
        id (str): 로그 ID (UUID)
        user_id (str): 사용자 ID
        credit_change (int): 크레딧 변동량
        change_type (str): 변동 유형 (사용/충전/환불)
        description (str): 변동 사유
        created_at (datetime): 생성 시간
    """
    __tablename__ = "user_credit_log"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    credit_change = Column(Integer)
    change_type = Column(String)  # '사용', '충전', '환불'
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    user = relationship("User", back_populates="credit_logs")

class SystemLog(Base):
    """
    시스템 운영 로그를 기록하는 테이블
    
    Attributes:
        id (str): 로그 ID (UUID)
        log_type (str): 로그 유형 (에러/경고/정보)
        message (str): 로그 메시지
        details (str): 상세 정보
        created_at (datetime): 생성 시간
    """
    __tablename__ = "system_log"

    id = Column(String, primary_key=True, index=True)
    log_type = Column(String)  # '에러', '경고', '정보'
    message = Column(String)
    details = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 