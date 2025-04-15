from typing import List, Dict, Any
import time
import requests
from bs4 import BeautifulSoup
from ..config import Config
from ....utils.text_cleaner import clean_text

class DcinsideCrawler:
    def __init__(self):
        """Initialize DC Inside crawler"""
        self.base_url = "https://search.dcinside.com"
        self.search_url = f"{self.base_url}/search"
    
    async def crawl(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Crawl DC Inside for posts related to the keyword
        
        Args:
            keyword: The keyword to search for
            
        Returns:
            List of dictionaries containing post information
        """
        try:
            # Simulate API delay
            await time.sleep(1)
            
            # Search DC Inside
            params = {
                "q": keyword,
                "type": "post",
                "sort": "date"
            }
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            response = requests.get(self.search_url, params=params, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for post in soup.select('.search_list li'):
                title_elem = post.select_one('.tit')
                if not title_elem:
                    continue
                    
                results.append({
                    "source": "dcinside",
                    "title": title_elem.text.strip(),
                    "url": title_elem['href'],
                    "author": post.select_one('.user').text.strip() if post.select_one('.user') else None,
                    "date": post.select_one('.date').text.strip() if post.select_one('.date') else None,
                    "gall_name": post.select_one('.gall_name').text.strip() if post.select_one('.gall_name') else None
                })
            
            return results
            
        except Exception as e:
            raise Exception(f"디시인사이드 크롤링 중 오류 발생: {str(e)}")

async def crawl_dcinside(input_text: str) -> List[str]:
    # TODO: 실제 크롤링 구현 예정
    # 현재는 테스트용 샘플 데이터 반환
    raw_text = f"[dcinside] 크롤링 결과 샘플: '{input_text}' <p>HTML 태그 테스트</p> https://gall.dcinside.com 👍"
    return [clean_text(raw_text)] 