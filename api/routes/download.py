from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from api.services.exporter import EXPORT_DIR

router = APIRouter()

@router.get("/{filename}")
async def download_file(filename: str):
    """
    저장된 HTML 파일을 다운로드합니다.
    
    Args:
        filename: 다운로드할 파일명
        
    Returns:
        FileResponse: 파일 다운로드 응답
        
    Raises:
        HTTPException: 파일이 존재하지 않을 경우
    """
    filepath = os.path.join(EXPORT_DIR, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
        
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="text/html"
    ) 