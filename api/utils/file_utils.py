import os
import glob
from typing import Optional
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

# Constants
EXPORT_DIR_HTML = "exported_reports"
EXPORT_DIR_PDF = "exported_pdfs"

def ensure_export_directories():
    """
    내보내기에 필요한 디렉토리들이 존재하는지 확인하고 없으면 생성합니다.
    """
    try:
        os.makedirs(EXPORT_DIR_HTML, exist_ok=True)
        os.makedirs(EXPORT_DIR_PDF, exist_ok=True)
        logger.info(f"내보내기 디렉토리 확인 완료: {EXPORT_DIR_HTML}, {EXPORT_DIR_PDF}")
    except Exception as e:
        logger.error(f"내보내기 디렉토리 생성 중 오류: {str(e)}")
        raise

def find_latest_html_filename(analysis_id: str) -> Optional[str]:
    """
    주어진 분석 ID에 대한 가장 최근 HTML 파일명을 찾습니다.
    
    Args:
        analysis_id (str): 분석 ID
        
    Returns:
        Optional[str]: 가장 최근 HTML 파일명 또는 None
    """
    try:
        pattern = f"{EXPORT_DIR_HTML}/{analysis_id}_*.html"
        files = glob.glob(pattern)
        
        if not files:
            logger.debug(f"HTML 파일을 찾을 수 없음: {pattern}")
            return None
            
        latest_file = max(files, key=os.path.getctime)
        filename = os.path.basename(latest_file)
        logger.debug(f"HTML 파일 찾음: {filename}")
        return filename
        
    except Exception as e:
        logger.error(f"HTML 파일명 검색 중 오류: {str(e)}")
        return None

def find_latest_pdf_filename(analysis_id: str) -> Optional[str]:
    """
    주어진 분석 ID에 대한 가장 최근 PDF 파일명을 찾습니다.
    
    Args:
        analysis_id (str): 분석 ID
        
    Returns:
        Optional[str]: 가장 최근 PDF 파일명 또는 None
    """
    try:
        pattern = f"{EXPORT_DIR_PDF}/{analysis_id}_*.pdf"
        files = glob.glob(pattern)
        
        if not files:
            logger.debug(f"PDF 파일을 찾을 수 없음: {pattern}")
            return None
            
        latest_file = max(files, key=os.path.getctime)
        filename = os.path.basename(latest_file)
        logger.debug(f"PDF 파일 찾음: {filename}")
        return filename
        
    except Exception as e:
        logger.error(f"PDF 파일명 검색 중 오류: {str(e)}")
        return None

def cleanup_old_files(max_age_days: int = 7) -> None:
    """
    지정된 기간보다 오래된 파일들을 삭제합니다.
    
    Args:
        max_age_days (int): 최대 보관 기간(일)
    """
    try:
        current_time = datetime.now()
        for directory in [EXPORT_DIR_HTML, EXPORT_DIR_PDF]:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                    age_days = (current_time - file_time).days
                    
                    if age_days > max_age_days:
                        os.remove(filepath)
                        logger.info(f"오래된 파일 삭제: {filepath}")
                        
    except Exception as e:
        logger.error(f"오래된 파일 정리 중 오류: {str(e)}") 