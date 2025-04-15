from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from typing import List, Optional
from api.services.exporter import EXPORT_DIR
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Constants
PDF_EXPORT_DIR = "exported_pdfs"
os.makedirs(PDF_EXPORT_DIR, exist_ok=True)

@router.get("/download/{filename}")
async def download_report(filename: str):
    """
    저장된 HTML 파일 다운로드
    
    Args:
        filename: 다운로드할 파일명
    
    Returns:
        FileResponse: HTML 파일
    """
    try:
        file_path = os.path.join(EXPORT_DIR, filename)
        
        # 파일 존재 여부 확인
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail="요청한 파일을 찾을 수 없습니다."
            )
        
        # 파일 다운로드
        return FileResponse(
            file_path,
            media_type="text/html",
            filename=filename,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"파일 다운로드 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/list")
async def list_reports() -> List[str]:
    """
    저장된 HTML 파일 목록 조회
    
    Returns:
        List[str]: 파일명 목록
    """
    try:
        if not os.path.exists(EXPORT_DIR):
            return []
        
        files = [
            f for f in os.listdir(EXPORT_DIR)
            if f.endswith(".html")
        ]
        return sorted(files, reverse=True)  # 최신순 정렬
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"파일 목록 조회 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/download/pdf/{filename}")
async def download_pdf(filename: str) -> FileResponse:
    """
    PDF 파일을 다운로드하는 엔드포인트
    
    Args:
        filename (str): 다운로드할 PDF 파일명
        
    Returns:
        FileResponse: PDF 파일 응답
        
    Raises:
        HTTPException: 파일이 존재하지 않을 경우 404 에러
    """
    try:
        file_path = os.path.join(PDF_EXPORT_DIR, filename)
        
        # 파일 존재 여부 확인
        if not os.path.exists(file_path):
            logger.error(f"PDF 파일을 찾을 수 없음: {filename}")
            raise HTTPException(
                status_code=404,
                detail="PDF 파일이 존재하지 않습니다."
            )
            
        # 파일 확장자 검증
        if not filename.lower().endswith('.pdf'):
            logger.error(f"잘못된 파일 형식: {filename}")
            raise HTTPException(
                status_code=400,
                detail="잘못된 파일 형식입니다. PDF 파일만 다운로드 가능합니다."
            )
            
        logger.info(f"PDF 파일 다운로드 시작: {filename}")
        return FileResponse(
            file_path,
            media_type="application/pdf",
            filename=filename,
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF 다운로드 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="PDF 다운로드 중 오류가 발생했습니다."
        ) 