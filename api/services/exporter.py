from datetime import datetime
import os
import json
from typing import Dict, Any, Optional

# HTML 템플릿
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>분석 결과 - {analysis_id}</title>
    <style>
        body {{
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            border-bottom: 2px solid #eee;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .title {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .meta {{
            color: #666;
            font-size: 14px;
        }}
        .content {{
            margin-top: 20px;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section-title {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #2c5282;
        }}
        .item {{
            margin-bottom: 15px;
            padding: 15px;
            background-color: #f8fafc;
            border-radius: 8px;
        }}
        .item-title {{
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .item-content {{
            white-space: pre-wrap;
        }}
        @media print {{
            body {{
                padding: 0;
            }}
            .item {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">분석 결과</div>
        <div class="meta">
            <div>분석 ID: {analysis_id}</div>
            <div>생성일: {created_at}</div>
        </div>
    </div>
    <div class="content">
        {content}
    </div>
</body>
</html>
"""

def format_result_content(result_json: str) -> str:
    """분석 결과 JSON을 HTML 형식으로 변환"""
    try:
        result = json.loads(result_json)
        html_content = ""
        
        for section_title, items in result.items():
            html_content += f'<div class="section">'
            html_content += f'<div class="section-title">{section_title}</div>'
            
            if isinstance(items, list):
                for item in items:
                    html_content += '<div class="item">'
                    if isinstance(item, dict):
                        for key, value in item.items():
                            html_content += f'<div class="item-title">{key}</div>'
                            html_content += f'<div class="item-content">{value}</div>'
                    else:
                        html_content += f'<div class="item-content">{item}</div>'
                    html_content += '</div>'
            else:
                html_content += f'<div class="item-content">{items}</div>'
            
            html_content += '</div>'
        
        return html_content
    except json.JSONDecodeError:
        return f'<div class="item-content">{result_json}</div>'

# HTML 파일 저장 디렉토리
EXPORT_DIR = "exports"
if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

def save_result_as_html(analysis_id: str, html_content: str) -> str:
    """
    분석 결과를 HTML 파일로 저장
    
    Args:
        analysis_id: 분석 ID
        html_content: HTML 내용
        
    Returns:
        str: 저장된 파일 경로
    """
    try:
        # 파일명 생성 (분석ID_타임스탬프.html)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{analysis_id}_{timestamp}.html"
        filepath = os.path.join(EXPORT_DIR, filename)
        
        # HTML 파일 저장
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        return filepath
        
    except Exception as e:
        raise Exception(f"HTML 저장 중 오류 발생: {str(e)}")

def get_html_file(analysis_id: str) -> Optional[str]:
    """
    분석 ID에 해당하는 HTML 파일 경로 반환
    
    Args:
        analysis_id: 분석 ID
        
    Returns:
        Optional[str]: 파일 경로 (없으면 None)
    """
    try:
        # 분석 ID로 시작하는 가장 최근 파일 찾기
        files = [
            f for f in os.listdir(EXPORT_DIR)
            if f.startswith(analysis_id) and f.endswith(".html")
        ]
        
        if not files:
            return None
            
        # 가장 최근 파일 반환
        latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(EXPORT_DIR, x)))
        return os.path.join(EXPORT_DIR, latest_file)
        
    except Exception as e:
        raise Exception(f"HTML 파일 조회 중 오류 발생: {str(e)}")

def get_latest_html_file(analysis_id: str) -> Optional[str]:
    """
    주어진 analysis_id에 해당하는 가장 최근 HTML 파일 경로를 반환합니다.
    
    Args:
        analysis_id: 분석 ID
        
    Returns:
        Optional[str]: 파일 경로 (파일이 없으면 None)
    """
    try:
        # exported_reports 디렉토리에서 해당 ID로 시작하는 파일들 찾기
        files = [f for f in os.listdir(EXPORT_DIR) 
                if f.startswith(f"{analysis_id}_") and f.endswith(".html")]
        
        if not files:
            return None
            
        # 가장 최근 파일 선택 (타임스탬프가 가장 큰 파일)
        latest_file = max(files)
        return os.path.join(EXPORT_DIR, latest_file)
        
    except Exception as e:
        print(f"Error getting latest HTML file: {str(e)}")
        return None 