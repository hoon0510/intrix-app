from weasyprint import HTML
from datetime import datetime
import os
import tempfile
from typing import Dict, Any
from .formatter import render_html
import logging

logger = logging.getLogger(__name__)

def generate_pdf(data: Dict[str, Any]) -> str:
    """
    분석 결과를 PDF로 변환합니다.
    
    Args:
        data (Dict[str, Any]): 리포트 데이터
        
    Returns:
        str: 생성된 PDF 파일 경로
        
    Raises:
        Exception: PDF 생성 중 오류 발생 시
    """
    temp_file = None
    try:
        # HTML 렌더링
        html_content = render_html({
            **data,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "current_year": datetime.now().year
        })
        
        # 임시 파일 생성
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf",
            dir=os.path.join(os.path.dirname(__file__), "../../temp")
        )
        
        # PDF 생성
        HTML(
            string=html_content,
            base_url=os.path.dirname(__file__)
        ).write_pdf(temp_file.name)
        
        logger.info(f"PDF 생성 완료: {temp_file.name}")
        return temp_file.name
        
    except Exception as e:
        # 오류 발생 시 임시 파일 정리
        if temp_file and os.path.exists(temp_file.name):
            try:
                os.unlink(temp_file.name)
            except:
                pass
        logger.error(f"PDF 생성 중 오류 발생: {str(e)}")
        raise Exception(f"PDF 생성 중 오류 발생: {str(e)}")
        
    finally:
        if temp_file:
            temp_file.close() 