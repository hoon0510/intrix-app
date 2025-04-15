import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

# 로그 디렉토리 설정
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# 로그 파일 경로 설정 (일별 로그 파일)
LOG_FILE = os.path.join(LOG_DIR, f"intrix_{datetime.now().strftime('%Y%m%d')}.log")

def configure_logging():
    """
    로깅 설정을 구성합니다.
    - 콘솔과 파일에 동시 로깅
    - 파일은 일별로 생성되며, 최대 5MB까지 저장
    - 백업 파일은 3개까지 유지
    """
    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # 콘솔 핸들러 설정
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 파일 핸들러 설정
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)

    # 로그 포맷 설정
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s [%(name)s] - %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 핸들러 추가
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # FastAPI 액세스 로거 설정
    access_logger = logging.getLogger("uvicorn.access")
    access_logger.setLevel(logging.INFO)
    access_logger.addHandler(console_handler)
    access_logger.addHandler(file_handler)

    # 에러 로거 설정
    error_logger = logging.getLogger("uvicorn.error")
    error_logger.setLevel(logging.INFO)
    error_logger.addHandler(console_handler)
    error_logger.addHandler(file_handler)

    return root_logger 