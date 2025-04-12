"""
Crawler Dispatcher
"""

import importlib
import os
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

class CrawlerDispatcher:
    def __init__(self):
        self.crawler_dir = os.path.dirname(__file__)
        self.available_crawlers = {
            # Community channels
            "reddit": "reddit_scraper",
            "ppomppu": "ppomppu_scraper",
            "fmkorea": "fmkorea_scraper",
            "dcinside": "dc_scraper",
            "theqoo": "theqoo_scraper",
            "mlbpark": "mlbpark_scraper",
            "ruliweb": "ruliweb_scraper",
            "inven": "inven_scraper",
            "arca": "arca_scraper",
            "clien": "clien_scraper",
            
            # SNS channels
            "instagram": "instagram_scraper",
            "threads": "threads_scraper",
            "youtube": "youtube_scraper",
            "facebook": "facebook_scraper",
            "x": "x_scraper"
        }
        
    def _load_crawler(self, channel: str):
        """
        Dynamically load a crawler module for the specified channel
        
        Args:
            channel: Channel name to load crawler for
            
        Returns:
            Crawler module instance
        """
        if channel not in self.available_crawlers:
            raise ValueError(f"Unsupported channel: {channel}")
            
        module_name = self.available_crawlers[channel]
        try:
            module = importlib.import_module(f"crawlers.{module_name}")
            return module.Crawler()
        except ImportError:
            raise ImportError(f"Failed to load crawler for {channel}")
            
    async def crawl_channel(self, channel: str, keyword: str) -> Dict:
        """
        Crawl a single channel
        
        Args:
            channel: Channel name to crawl
            keyword: Search keyword
            
        Returns:
            Dictionary containing crawl results
        """
        try:
            crawler = self._load_crawler(channel)
            results = await crawler.crawl(keyword)
            return {
                "channel": channel,
                "status": "success",
                "results": results
            }
        except Exception as e:
            return {
                "channel": channel,
                "status": "error",
                "error": str(e)
            }
            
    async def crawl_channels(
        self,
        keyword: str,
        community_channels: List[str],
        sns_channels: List[str],
        max_workers: int = 5
    ) -> Dict:
        """
        Crawl multiple channels concurrently
        
        Args:
            keyword: Search keyword
            community_channels: List of community channels to crawl
            sns_channels: List of SNS channels to crawl
            max_workers: Maximum number of concurrent workers
            
        Returns:
            Dictionary containing results from all channels
        """
        all_channels = community_channels + sns_channels
        results = {
            "community": {},
            "sns": {}
        }
        
        # Validate channels
        invalid_channels = [
            channel for channel in all_channels 
            if channel not in self.available_crawlers
        ]
        if invalid_channels:
            raise ValueError(f"Invalid channels: {', '.join(invalid_channels)}")
            
        # Execute crawlers concurrently
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.crawl_channel, channel, keyword): channel
                for channel in all_channels
            }
            
            for future in as_completed(futures):
                channel = futures[future]
                try:
                    result = future.result()
                    if result["status"] == "success":
                        if channel in community_channels:
                            results["community"][channel] = result["results"]
                        else:
                            results["sns"][channel] = result["results"]
                except Exception as e:
                    if channel in community_channels:
                        results["community"][channel] = {"error": str(e)}
                    else:
                        results["sns"][channel] = {"error": str(e)}
                        
        return results 