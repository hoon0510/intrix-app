"""
PDF Download Handler Service
"""

from fastapi import HTTPException
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
import os
from datetime import datetime

async def download_pdf(input_html: str) -> bytes:
    """
    Convert HTML to PDF using WeasyPrint
    
    Args:
        input_html: HTML content to convert
        
    Returns:
        bytes: PDF file content
        
    Raises:
        HTTPException: If PDF generation fails
    """
    try:
        # Configure fonts
        font_config = FontConfiguration()
        
        # Create HTML object
        html = HTML(string=input_html)
        
        # Generate PDF
        pdf_bytes = html.write_pdf(font_config=font_config)
        
        return pdf_bytes
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate PDF: {str(e)}"
        )

async def save_pdf(input_html: str, filename: str = None) -> str:
    """
    Save HTML as PDF file
    
    Args:
        input_html: HTML content to convert
        filename: Optional filename (default: timestamp-based)
        
    Returns:
        str: Path to the saved PDF file
        
    Raises:
        HTTPException: If PDF generation or saving fails
    """
    try:
        # Generate PDF bytes
        pdf_bytes = await download_pdf(input_html)
        
        # Create filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.pdf"
        
        # Ensure filename has .pdf extension
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        
        # Create reports directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)
        
        # Save PDF file
        filepath = os.path.join('reports', filename)
        with open(filepath, 'wb') as f:
            f.write(pdf_bytes)
        
        return filepath
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save PDF: {str(e)}"
        ) 