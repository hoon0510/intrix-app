from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

def register_exception_handlers(app):
    """
    FastAPI 앱에 글로벌 예외 핸들러를 등록합니다.
    모든 예외를 일관된 형식으로 처리하고 로깅합니다.
    """
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """HTTP 예외를 처리하는 핸들러"""
        logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "code": exc.status_code,
                "type": "http_error"
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """요청 검증 예외를 처리하는 핸들러"""
        logger.warning(f"Validation Error: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={
                "error": "요청 형식이 잘못되었습니다.",
                "details": exc.errors(),
                "type": "validation_error"
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """일반적인 예외를 처리하는 핸들러"""
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "내부 서버 오류가 발생했습니다.",
                "detail": str(exc),
                "type": "server_error"
            },
        ) 