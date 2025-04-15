from typing import List, Dict, Any
import time
import requests
from bs4 import BeautifulSoup
from ..config import Config
from ....utils.text_cleaner import clean_text
import logging

logger = logging.getLogger(__name__)

class PpomppuCrawler:
    def __init__(self):
        """Initialize Ppomppu crawler"""
        self.base_url = "https://www.ppomppu.co.kr"
        self.search_url = f"{self.base_url}/search_bbs.php"
    
    async def crawl(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Crawl Ppomppu for posts related to the keyword
        
        Args:
            keyword: The keyword to search for
            
        Returns:
            List of dictionaries containing post information
        """
        try:
            # Simulate API delay
            await time.sleep(1)
            
            # Search Ppomppu
            params = {
                "keyword": keyword,
                "category": "",
                "page": 1
            }
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            logger.info(f"[PPOMPPU] 크롤링 시작: {keyword}")
            start_time = time.time()
            
            # 타임아웃 5초로 설정하여 요청
            response = requests.get(self.search_url, params=params, headers=headers, timeout=5)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for post in soup.select('.board-item'):
                title_elem = post.select_one('.title')
                if not title_elem:
                    continue
                    
                results.append({
                    "source": "ppomppu",
                    "title": title_elem.text.strip(),
                    "url": f"{self.base_url}{title_elem['href']}",
                    "author": post.select_one('.author').text.strip() if post.select_one('.author') else None,
                    "date": post.select_one('.date').text.strip() if post.select_one('.date') else None,
                    "views": post.select_one('.views').text.strip() if post.select_one('.views') else None
                })
            
            elapsed_time = time.time() - start_time
            logger.info(f"[PPOMPPU] 크롤링 완료: {len(results)}개 결과, {elapsed_time:.2f}초 소요")
            return results
            
        except requests.exceptions.Timeout:
            logger.warning(f"[PPOMPPU] 요청 시간 초과: {keyword}")
            return []
        
        except requests.exceptions.RequestException as e:
            logger.error(f"[PPOMPPU] 요청 실패: {str(e)}")
            return []
        
        except Exception as e:
            logger.error(f"[PPOMPPU] 예상치 못한 오류: {str(e)}")
            return []

async def crawl_ppomppu(keyword: str) -> List[Dict[str, Any]]:
    """
    뽐뿌에서 키워드 관련 게시물을 크롤링합니다.
    
    Args:
        keyword (str): 검색할 키워드
        
    Returns:
        List[Dict[str, Any]]: 크롤링 결과 리스트
    """
    try:
        # 검색 URL 설정
        url = "https://www.ppomppu.co.kr/search_bbs.php"
        params = {
            "search_type": "sub_memo",
            "keyword": keyword,
            "page": 1
        }
        
        # 요청 헤더 설정
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        logger.info(f"[PPOMPPU] 크롤링 시작: {keyword}")
        start_time = time.time()
        
        # 타임아웃 5초로 설정하여 요청
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        
        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.select('.board_list .list')
        
        # 결과 가공
        results = []
        for post in posts:
            title_elem = post.select_one('.title')
            content_elem = post.select_one('.content')
            date_elem = post.select_one('.date')
            
            if title_elem and content_elem:
                results.append({
                    "title": title_elem.get_text(strip=True),
                    "content": content_elem.get_text(strip=True),
                    "date": date_elem.get_text(strip=True) if date_elem else "",
                    "url": f"https://www.ppomppu.co.kr{title_elem.get('href', '')}"
                })
        
        elapsed_time = time.time() - start_time
        logger.info(f"[PPOMPPU] 크롤링 완료: {len(results)}개 결과, {elapsed_time:.2f}초 소요")
        return results
        
    except requests.exceptions.Timeout:
        logger.warning(f"[PPOMPPU] 요청 시간 초과: {keyword}")
        return []
        
    except requests.exceptions.RequestException as e:
        logger.error(f"[PPOMPPU] 요청 실패: {str(e)}")
        return []
        
    except Exception as e:
        logger.error(f"[PPOMPPU] 예상치 못한 오류: {str(e)}")
        return [] 