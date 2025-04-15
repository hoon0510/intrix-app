from fastapi import Request
from fastapi.responses import JSONResponse
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

async def global_error_handler(request: Request, exc: Exception):
    # Log the error with stack trace
    logger.error(f"Unhandled error: {str(exc)}")
    logger.error(f"Stack trace: {traceback.format_exc()}")
    
    # Return a structured error response
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc),
            "path": request.url.path,
            "method": request.method
        }
    ) 