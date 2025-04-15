from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from pydantic import BaseModel
import os
import logging
from api.services.exporter import save_result_as_html
from api.services.pdf_exporter import save_html_as_pdf
from api.utils.auth import get_current_user
from api.services.claude import claude_formatting_function

# 로거 설정
logger = logging.getLogger(__name__)

router = APIRouter()

class FormatRequest(BaseModel):
    analysis_id: str
    strategy: Dict[str, Any]
    analysis: Dict[str, Any]
    copy: Dict[str, Any]

class FormatResponse(BaseModel):
    formatted_html: str
    html_filename: Optional[str] = None
    pdf_filename: Optional[str] = None

@router.post("/format", response_model=FormatResponse)
async def format_report(
    data: FormatRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Format strategy, analysis, and copy into HTML report
    
    Args:
        data: FormatRequest containing analysis_id, strategy, analysis, and copy
        current_user: Current authenticated user
        
    Returns:
        FormatResponse containing formatted HTML and download filenames
        
    Raises:
        HTTPException: If formatting or saving fails
    """
    try:
        logger.info(f"Starting HTML formatting for analysis_id: {data.analysis_id}")
        
        # Format the content using Claude
        html_result = await claude_formatting_function(
            strategy=data.strategy,
            analysis=data.analysis,
            copy=data.copy
        )
        
        logger.info(f"HTML formatting completed for analysis_id: {data.analysis_id}")
        
        # Save HTML to file
        html_filepath = save_result_as_html(data.analysis_id, html_result)
        logger.info(f"HTML saved to file: {html_filepath}")
        
        # Save PDF
        pdf_path = save_html_as_pdf(data.analysis_id, html_result)
        
        if not pdf_path:
            logger.error(f"PDF 저장 실패: {data.analysis_id}")
            raise HTTPException(
                status_code=500,
                detail="PDF 저장 중 오류가 발생했습니다."
            )
            
        logger.info(f"포맷팅 완료 - HTML: {html_filepath}, PDF: {pdf_path}")
        
        return FormatResponse(
            formatted_html=html_result,
            html_filename=os.path.basename(html_filepath),
            pdf_filename=os.path.basename(pdf_path)
        )
        
    except Exception as e:
        logger.error(f"Error formatting report for analysis_id {data.analysis_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Report formatting failed: {str(e)}"
        ) 