"""
Download endpoint router for PDF report generation.
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import Dict
import os
from ..services.download_handler import DownloadHandler

router = APIRouter(prefix="/download", tags=["download"])
download_handler = DownloadHandler()

class DownloadRequest:
    """Request model for full report download."""
    report_html: str
    copy: str
    style: str
    reference_point: str
    frame_shift: str
    positioning: str

@router.post("/full-report")
async def download_full_report(request: DownloadRequest):
    """
    Generates and downloads a PDF report containing the full analysis.
    
    Args:
        request: DownloadRequest containing report data
        
    Returns:
        FileResponse: PDF file download
        
    Raises:
        HTTPException: If PDF generation fails
    """
    try:
        # Convert request to dictionary
        data = {
            "report_html": request.report_html,
            "copy": request.copy,
            "style": request.style,
            "reference_point": request.reference_point,
            "frame_shift": request.frame_shift,
            "positioning": request.positioning
        }
        
        # Generate PDF
        pdf_path = download_handler.generate_pdf(data)
        
        # Return file response
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename="marketing-strategy-report.pdf",
            background=None  # This ensures cleanup after response is sent
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate PDF: {str(e)}"
        )
    finally:
        # Cleanup PDF file
        if 'pdf_path' in locals():
            download_handler.cleanup(pdf_path) 