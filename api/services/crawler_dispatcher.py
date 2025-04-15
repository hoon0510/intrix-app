import logging
from typing import Dict, List, Optional
from api.routes.crawler import CRAWLER_MAP
from api.utils.cache import get_cache, set_cache
from api.utils.text_cleaner import filter_short_results
from api.constants.channel_config import format_result_with_channel

logger = logging.getLogger("uvicorn.access")

class CrawlerDispatcher:
    async def run_selected_crawlers(
        self,
        channels: List[str],
        input_text: str,
        user_id: str
    ) -> List[Dict]:
        """
        선택된 채널들의 크롤러를 실행하고 결과를 반환합니다.
        """
        results = []
        channel_stats = {}
        
        for channel in channels:
            try:
                if channel not in CRAWLER_MAP:
                    logger.warning(f"[CRAWLER] 지원하지 않는 채널: {channel}")
                    channel_stats[channel] = 0
                    continue
                
                crawler_func = CRAWLER_MAP[channel]
                logger.info(f"[CRAWLER] 채널 {channel} 크롤링 시작")
                
                channel_results = await crawler_func(input_text)
                if not channel_results:
                    logger.warning(f"[CRAWLER] 채널 {channel}에서 결과를 찾을 수 없음")
                    channel_stats[channel] = 0
                    continue
                
                # 채널 라벨 추가
                labeled_results = []
                for result in channel_results:
                    try:
                        labeled_result = {
                            "title": format_result_with_channel(channel, result["title"]),
                            "content": format_result_with_channel(channel, result["content"]),
                            "url": result["url"]
                        }
                        labeled_results.append(labeled_result)
                    except Exception as e:
                        logger.error(f"[CRAWLER] 결과 포맷팅 실패: 채널={channel}, 결과={result}, 에러={str(e)}")
                        continue
                
                results.extend(labeled_results)
                channel_stats[channel] = len(labeled_results)
                logger.info(f"[CRAWLER] 채널 {channel} 크롤링 완료: {len(labeled_results)}개 결과")
                
            except Exception as e:
                logger.error(f"[CRAWLER ERROR] 채널={channel}, 입력값={input_text}, 에러={str(e)}", exc_info=True)
                channel_stats[channel] = 0
                continue
        
        # 중복 제거
        unique_results = []
        seen = set()
        for result in results:
            key = f"{result['title']}{result['content']}"
            if key not in seen:
                seen.add(key)
                unique_results.append(result)
        
        # 짧은 결과 필터링
        filtered_results = filter_short_results(unique_results)
        
        # 최대 결과 수 제한
        MAX_RESULT_COUNT = 30
        final_results = filtered_results[:MAX_RESULT_COUNT]
        
        # 캐시에 저장
        cache_key = f"crawl:{input_text}:{','.join(channels)}"
        set_cache(cache_key, final_results)
        
        logger.info(f"[CRAWLER] 최종 결과: {len(final_results)}개 (중복 제거: {len(results) - len(unique_results)}개, 필터링: {len(unique_results) - len(filtered_results)}개)")
        
        return final_results, channel_stats 