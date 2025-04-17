from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# 템플릿 디렉토리 설정
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "../../templates")

# Jinja2 환경 설정
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(['html', 'xml']),
    trim_blocks=True,
    lstrip_blocks=True
)

def render_html(data: Dict[str, Any]) -> str:
    """
    데이터를 HTML 템플릿에 렌더링합니다.
    
    Args:
        data (Dict[str, Any]): 템플릿에 전달할 데이터
        
    Returns:
        str: 렌더링된 HTML 문자열
        
    Raises:
        Exception: 템플릿 렌더링 중 오류 발생 시
    """
    try:
        template = env.get_template("report_base.html")
        return template.render(**data)
    except Exception as e:
        logger.error(f"HTML 렌더링 중 오류 발생: {str(e)}")
        raise Exception(f"HTML 렌더링 중 오류 발생: {str(e)}") 