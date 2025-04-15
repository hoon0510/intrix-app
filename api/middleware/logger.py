import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Awaitable
import json
from datetime import datetime
import os

# 로그 디렉토리 생성
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 파일 핸들러 설정
file_handler = logging.FileHandler(
    filename=os.path.join(log_dir, f"api_{datetime.now().strftime('%Y%m%d')}.log"),
    encoding="utf-8"
)
file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
)

# 로거 설정
logger = logging.getLogger("api")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable]
    ) -> Awaitable:
        # 요청 시작 시간 기록
        start_time = time.time()
        
        # 요청 정보 로깅
        request_info = {
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "client": request.client.host if request.client else None,
            "timestamp": datetime.now().isoformat()
        }
        
        # 요청 본문 로깅 (POST, PUT, PATCH 요청의 경우)
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    request_info["body"] = body.decode()
            except Exception as e:
                request_info["body_error"] = str(e)
        
        logger.info(f"Request: {json.dumps(request_info, ensure_ascii=False)}")
        
        # 응답 처리
        response = await call_next(request)
        
        # 응답 정보 로깅
        response_info = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "duration": time.time() - start_time,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Response: {json.dumps(response_info, ensure_ascii=False)}")
        
        return response 