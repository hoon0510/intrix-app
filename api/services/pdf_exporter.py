from weasyprint import HTML
import os
from datetime import datetime
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
PDF_EXPORT_DIR = "exported_pdfs"
os.makedirs(PDF_EXPORT_DIR, exist_ok=True)

def save_html_as_pdf(analysis_id: str, html_content: str) -> Optional[str]:
    """
    Convert HTML content to PDF and save it to the export directory.
    
    Args:
        analysis_id (str): Unique identifier for the analysis
        html_content (str): HTML content to convert to PDF
        
    Returns:
        Optional[str]: Path to the generated PDF file, or None if conversion fails
    """
    try:
        # Generate filename with timestamp
        filename = f"{analysis_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        filepath = os.path.join(PDF_EXPORT_DIR, filename)
        
        # Convert HTML to PDF
        HTML(string=html_content).write_pdf(filepath)
        
        logger.info(f"PDF successfully generated: {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Error converting HTML to PDF: {str(e)}")
        return None

def cleanup_old_pdfs(max_age_days: int = 7) -> None:
    """
    Remove PDF files older than the specified number of days.
    
    Args:
        max_age_days (int): Maximum age of PDF files in days
    """
    try:
        current_time = datetime.now()
        for filename in os.listdir(PDF_EXPORT_DIR):
            filepath = os.path.join(PDF_EXPORT_DIR, filename)
            if os.path.isfile(filepath):
                file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                age_days = (current_time - file_time).days
                
                if age_days > max_age_days:
                    os.remove(filepath)
                    logger.info(f"Removed old PDF file: {filepath}")
                    
    except Exception as e:
        logger.error(f"Error cleaning up old PDF files: {str(e)}") 