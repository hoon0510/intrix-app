"""
Reddit Scraper Implementation
"""

import aiohttp
import asyncio
from typing import Dict, List
from .base_scraper import BaseScraper

class Crawler(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.reddit.com"
        self.search_url = f"{self.base_url}/search.json"
        
    async def crawl(self, keyword: str) -> Dict:
        """
        Crawl Reddit for the given keyword
        
        Args:
            keyword: Search keyword
            
        Returns:
            Dictionary containing crawl results
        """
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                params = {
                    "q": keyword,
                    "sort": "relevance",
                    "limit": 100
                }
                
                async with session.get(self.search_url, params=params) as response:
                    if not self._validate_response(response):
                        raise Exception("Invalid response from Reddit API")
                        
                    data = await response.json()
                    posts = data.get("data", {}).get("children", [])
                    
                    results = []
                    for post in posts:
                        post_data = post.get("data", {})
                        if not post_data:
                            continue
                            
                        cleaned_text = self._clean_text(post_data.get("selftext", ""))
                        if not cleaned_text:
                            continue
                            
                        result = {
                            "id": post_data.get("id"),
                            "title": post_data.get("title"),
                            "text": cleaned_text,
                            "url": post_data.get("url"),
                            "score": post_data.get("score"),
                            "created_utc": post_data.get("created_utc"),
                            "subreddit": post_data.get("subreddit"),
                            "keywords": self._extract_keywords(cleaned_text)
                        }
                        results.append(result)
                        
                    return {
                        "total_posts": len(results),
                        "posts": results
                    }
                    
        except Exception as e:
            raise Exception(f"Reddit crawling failed: {str(e)}")
            
    def _clean_text(self, text: str) -> str:
        """
        Clean Reddit-specific text
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        # Remove markdown formatting
        text = text.replace("**", "").replace("*", "").replace("~~", "")
        
        # Remove URLs
        text = " ".join(word for word in text.split() if not word.startswith("http"))
        
        # Remove special characters
        text = "".join(char for char in text if char.isalnum() or char.isspace())
        
        return super()._clean_text(text)
        
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from Reddit text
        
        Args:
            text: Text to extract keywords from
            
        Returns:
            List of extracted keywords
        """
        # Implement Reddit-specific keyword extraction
        # This is a placeholder - implement your actual extraction logic
        words = text.lower().split()
        return [word for word in words if len(word) > 3] 