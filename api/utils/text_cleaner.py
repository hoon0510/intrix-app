import re
from typing import List, Dict, Any

def clean_text(text: str) -> str:
    """
    텍스트에서 HTML 태그와 특수 문자를 제거합니다.
    """
    # HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', text)
    # URL 제거
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # 이모지 제거
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
    # 연속된 공백을 하나로
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def filter_short_results(results: List[Dict[str, Any]], min_length: int = 10) -> List[Dict[str, Any]]:
    """
    크롤링 결과에서 너무 짧은 문장을 필터링합니다.
    
    Args:
        results (List[Dict[str, Any]]): 크롤링 결과 리스트
        min_length (int): 최소 길이 기준 (기본값: 10)
        
    Returns:
        List[Dict[str, Any]]: 필터링된 결과 리스트
    """
    filtered_results = []
    
    for result in results:
        # 제목과 본문을 결합하여 길이 체크
        content = f"{result.get('title', '')} {result.get('content', '')}".strip()
        
        # 길이가 기준보다 짧으면 건너뛰기
        if len(content) < min_length:
            continue
            
        filtered_results.append(result)
        
    return filtered_results

def clean_text_list(texts: List[str]) -> List[str]:
    """
    텍스트 리스트에 대해 일괄적으로 전처리를 수행하는 함수
    
    Args:
        texts: 전처리할 텍스트 리스트
        
    Returns:
        전처리된 텍스트 리스트
    """
    return [clean_text(text) for text in texts if text and clean_text(text)] 