import requests
import time
from typing import List, Dict, Any
import logging
from bs4 import BeautifulSoup
from ....utils.text_cleaner import clean_text
import random

logger = logging.getLogger(__name__)

async def crawl_reddit(keyword: str) -> List[Dict[str, Any]]:
    """
    Reddit에서 키워드 관련 게시물을 크롤링합니다.
    
    Args:
        keyword (str): 검색할 키워드
        
    Returns:
        List[Dict[str, Any]]: 크롤링 결과 리스트
    """
    try:
        # API 엔드포인트 설정
        url = "https://www.reddit.com/search.json"
        params = {
            "q": keyword,
            "sort": "relevance",
            "limit": 10
        }
        
        # 요청 헤더 설정
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        logger.info(f"[REDDIT] 크롤링 시작: {keyword}")
        start_time = time.time()
        
        # 타임아웃 5초로 설정하여 요청
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        
        # 응답 처리
        data = response.json()
        posts = data.get("data", {}).get("children", [])
        
        # 결과 가공
        results = []
        for post in posts:
            post_data = post.get("data", {})
            results.append({
                "title": post_data.get("title", ""),
                "content": post_data.get("selftext", ""),
                "url": post_data.get("url", ""),
                "score": post_data.get("score", 0),
                "created_utc": post_data.get("created_utc", 0)
            })
        
        elapsed_time = time.time() - start_time
        logger.info(f"[REDDIT] 크롤링 완료: {len(results)}개 결과, {elapsed_time:.2f}초 소요")
        return results
        
    except requests.exceptions.Timeout:
        logger.warning(f"[REDDIT] 요청 시간 초과: {keyword}")
        return []
        
    except requests.exceptions.RequestException as e:
        logger.error(f"[REDDIT] 요청 실패: {str(e)}")
        return []
        
    except Exception as e:
        logger.error(f"[REDDIT] 예상치 못한 오류: {str(e)}")
        return []

async def crawl_reddit_old(input_text: str) -> List[str]:
    """
    Reddit 검색 결과를 크롤링하는 함수
    
    Args:
        input_text: 검색할 텍스트
        
    Returns:
        크롤링된 텍스트 목록. 실패 시 빈 리스트 반환
    """
    try:
        # 검색 URL 구성
        encoded_query = requests.utils.quote(input_text)
        url = f"https://www.reddit.com/search/?q={encoded_query}&sort=relevance"
        
        # User-Agent 랜덤 선택 (차단 방지)
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]
        
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
        }
        
        print(f"[reddit_crawler] 요청 시작: {url}")
        
        # HTTP 요청 수행
        response = requests.get(
            url,
            headers=headers,
            timeout=10,
            allow_redirects=True
        )
        response.raise_for_status()
        
        # 429 (Too Many Requests) 체크
        if response.status_code == 429:
            print("[reddit_crawler] 요청 한도 초과 (429)")
            return []
            
        # HTML 파싱
        soup = BeautifulSoup(response.text, "html.parser")
        
        results = []
        
        # 게시물 제목 추출 (h3 태그)
        titles = soup.select("h3")
        for title in titles:
            text = clean_text(title.get_text())
            if text and len(text) > 10:  # 짧은 텍스트 필터링
                results.append(f"[제목] {text}")
            if len(results) >= 3:  # 최대 3개 제목
                break
                
        # 게시물 내용 추출 (div[data-testid="post-container"])
        posts = soup.select('div[data-testid="post-container"]')
        for post in posts:
            content = post.select_one('div[data-click-id="text"]')
            if content:
                text = clean_text(content.get_text())
                if text and len(text) > 20:  # 짧은 텍스트 필터링
                    results.append(f"[내용] {text}")
                if len(results) >= 5:  # 총 5개 결과 제한
                    break
        
        print(f"[reddit_crawler] 크롤링 완료: {len(results)}개 결과")
        
        # 결과가 없으면 샘플 응답
        if not results:
            print("[reddit_crawler] 결과 없음, 샘플 응답 반환")
            return [f"[reddit] 크롤링 결과 샘플: '{input_text}'"]
            
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"[reddit_crawler] HTTP 요청 실패: {str(e)}")
        return []
    except Exception as e:
        print(f"[reddit_crawler] 크롤링 실패: {str(e)}")
        return []
    finally:
        # 요청 간 딜레이
        time.sleep(random.uniform(1, 2)) 