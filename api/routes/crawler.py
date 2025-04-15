from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from ..services.cache_manager import cache_manager
from ..services.credit_manager import credit_manager
from ..crawlers.reddit_scraper import RedditScraper
from ..crawlers.twitter_scraper import TwitterScraper
from ..crawlers.instagram_scraper import InstagramScraper
from ..crawlers.facebook_scraper import FacebookScraper
from ..crawlers.linkedin_scraper import LinkedInScraper
from ..crawlers.youtube_scraper import YouTubeScraper
from ..crawlers.tiktok_scraper import TikTokScraper
from ..crawlers.pinterest_scraper import PinterestScraper
from ..crawlers.quora_scraper import QuoraScraper
from ..crawlers.medium_scraper import MediumScraper
from ..crawlers.github_scraper import GitHubScraper
from ..crawlers.stackoverflow_scraper import StackOverflowScraper
from ..crawlers.producthunt_scraper import ProductHuntScraper
from ..crawlers.hackernews_scraper import HackerNewsScraper
from ..crawlers.indiehackers_scraper import IndieHackersScraper
from ..crawlers.devto_scraper import DevToScraper
from ..crawlers.hashnode_scraper import HashnodeScraper
from ..constants.channel_config import is_valid_channel, get_channel_type, SNS_CHANNELS, COMMUNITY_CHANNELS, format_result_with_channel
import asyncio
import hashlib
import json
import os
from datetime import datetime

# 채널별 크롤러 함수 임포트
from ..services.crawlers.reddit_crawler import crawl_reddit
from ..services.crawlers.ppomppu_crawler import crawl_ppomppu
from ..services.crawlers.dcinside_crawler import crawl_dcinside
from ..services.crawlers.theqoo_crawler import crawl_theqoo
from ..services.crawlers.ruliweb_crawler import crawl_ruliweb
from ..services.crawlers.clien_crawler import crawl_clien

from ..utils.logger import crawl_logger
from ..services.rate_limiter import rate_limiter
from api.dependencies.auth import get_current_user_id

router = APIRouter()

# 채널별 크롤러 함수 매핑
CHANNEL_CRAWLER_MAP = {
    "reddit": crawl_reddit,
    "ppomppu": crawl_ppomppu,
    "dcinside": crawl_dcinside,
    "theqoo": crawl_theqoo,
    "ruliweb": crawl_ruliweb,
    "clien": crawl_clien
}

# 환경 변수에서 로깅 활성화 여부 확인
SAVE_CRAWL_RESULTS = os.getenv("SAVE_CRAWL_RESULTS", "false").lower() == "true"
CRAWL_LOG_DIR = os.getenv("CRAWL_LOG_DIR", "crawl_logs")

def save_crawl_result(user_id: str, input_text: str, channels: List[str], results: List[Dict[str, Any]]) -> None:
    """
    크롤링 결과를 JSON 파일로 저장합니다.
    
    Args:
        user_id (str): 사용자 ID
        input_text (str): 검색어
        channels (List[str]): 크롤링한 채널 목록
        results (List[Dict[str, Any]]): 크롤링 결과
    """
    if not SAVE_CRAWL_RESULTS:
        return
        
    try:
        # 타임스탬프 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 파일명 생성 (사용자ID_타임스탬프.json)
        filename = f"{CRAWL_LOG_DIR}/{user_id}_{timestamp}.json"
        
        # 디렉토리 생성
        os.makedirs(CRAWL_LOG_DIR, exist_ok=True)
        
        # 결과 저장
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "user_id": user_id,
                "input_text": input_text,
                "channels": channels,
                "timestamp": timestamp,
                "results": results
            }, f, ensure_ascii=False, indent=2)
            
        print(f"[CRAWL] 결과 저장 완료: {filename}")
        
    except Exception as e:
        print(f"[CRAWL] 결과 저장 실패: {str(e)}")

class CrawlRequest(BaseModel):
    user_id: str
    input_text: str
    channels: List[str]

class CrawlResponse(BaseModel):
    from_cache: bool
    final_credit: int
    used_channels: List[str]
    results: List[Dict[str, Any]]
    channel_stats: Dict[str, int]
    meta: Dict[str, Any]

    class Config:
        schema_extra = {
            "example": {
                "from_cache": False,
                "final_credit": 18,
                "used_channels": ["reddit", "dcinside"],
                "results": [
                    {
                        "title": "[Reddit] Example Title",
                        "content": "[Reddit] Example Content",
                        "url": "https://reddit.com/example"
                    },
                    {
                        "title": "[디씨인사이드] 예제 제목",
                        "content": "[디씨인사이드] 예제 내용",
                        "url": "https://dcinside.com/example"
                    }
                ],
                "channel_stats": {
                    "reddit": 5,
                    "dcinside": 4
                },
                "meta": {
                    "total_count": 9,
                    "average_length": 42.1,
                    "was_sampled": False,
                    "fail_rate_percent": 0.0
                }
            }
        }

# Claude 분석을 위한 최대 입력 개수 제한
MAX_ANALYSIS_INPUT_COUNT = 30

def calculate_metadata(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    크롤링 결과의 메타데이터 통계를 계산합니다.
    
    Args:
        results (List[Dict[str, Any]]): 크롤링 결과 리스트
        
    Returns:
        Dict[str, Any]: 메타데이터 통계
    """
    total_count = len(results)
    
    # 전체 텍스트 길이 계산 (제목 + 내용)
    total_length = sum(
        len(result.get("title", "")) + len(result.get("content", ""))
        for result in results
    )
    
    # 평균 길이 계산 (소수점 첫째 자리까지)
    average_length = round(total_length / total_count, 1) if total_count > 0 else 0
    
    return {
        "total_count": total_count,
        "average_length": average_length,
        "total_length": total_length
    }

@router.post("/crawl", response_model=CrawlResponse)
async def crawl_text(data: CrawlRequest, user_id: str = Depends(get_current_user_id)):
    try:
        # 요청 제한 확인
        try:
            rate_limiter.check_rate_limit(user_id)
        except Exception as e:
            print(f"[RATE_LIMIT] 사용자 {user_id} 요청 제한 초과")
            crawl_logger.log_error(
                user_id=user_id,
                input_text=data.input_text,
                channels=data.channels,
                error_type="RATE_LIMIT",
                error_message=str(e)
            )
            raise HTTPException(
                status_code=429,
                detail={
                    "message": str(e),
                    "stats": rate_limiter.get_user_stats(user_id)
                }
            )

        # 사용된 채널 목록 정렬
        used_channels = sorted(list(set(data.channels)))
        print(f"[CRAWL] 사용 채널: {', '.join(used_channels)}")

        # Debug logging for request details
        print(f"[CRAWL] 요청 채널: {data.channels}")
        print(f"[CRAWL] 입력 텍스트: {data.input_text}")
        print(f"[CRAWL] 사용자 ID: {user_id}")

        # Input text validation
        MAX_INPUT_LENGTH = 500
        if not data.input_text.strip():
            print("[CRAWL] 빈 입력 텍스트 요청 거부")
            crawl_logger.log_error(
                user_id=user_id,
                input_text=data.input_text,
                channels=data.channels,
                error_type="VALIDATION",
                error_message="입력 텍스트가 비어 있습니다"
            )
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "입력 텍스트가 비어 있습니다.",
                    "note": "검색할 키워드나 문장을 입력해주세요."
                }
            )

        if len(data.input_text) > MAX_INPUT_LENGTH:
            print(f"[CRAWL] 입력 텍스트 길이 초과: {len(data.input_text)}자")
            crawl_logger.log_error(
                user_id=user_id,
                input_text=data.input_text,
                channels=data.channels,
                error_type="VALIDATION",
                error_message=f"입력 텍스트 길이 초과: {len(data.input_text)}자"
            )
            raise HTTPException(
                status_code=413,
                detail={
                    "message": f"입력 텍스트는 최대 {MAX_INPUT_LENGTH}자까지 허용됩니다.",
                    "current_length": len(data.input_text),
                    "note": "더 짧은 키워드나 문장으로 다시 시도해주세요."
                }
            )

        # Check for empty channels
        if not data.channels:
            print("[CRAWL] 빈 채널 리스트 요청 거부")
            crawl_logger.log_error(
                user_id=user_id,
                input_text=data.input_text,
                channels=data.channels,
                error_type="VALIDATION",
                error_message="크롤링할 채널을 1개 이상 선택해야 합니다"
            )
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "크롤링할 채널을 1개 이상 선택해야 합니다.",
                    "supported_community_channels": COMMUNITY_CHANNELS,
                    "note": "커뮤니티 채널 중 최소 1개는 포함해야 합니다."
                }
            )

        # Check if all channels are SNS channels
        if all(ch in SNS_CHANNELS for ch in data.channels):
            print(f"[CRAWL] SNS 채널만 포함된 요청 거부: {data.channels}")
            crawl_logger.log_error(
                user_id=user_id,
                input_text=data.input_text,
                channels=data.channels,
                error_type="VALIDATION",
                error_message="선택된 채널이 모두 SNS 채널입니다"
            )
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "선택된 채널이 모두 SNS 채널입니다.",
                    "supported_community_channels": COMMUNITY_CHANNELS,
                    "note": "커뮤니티 채널 중 최소 1개는 포함해야 합니다."
                }
            )

        # Check for unsupported SNS channels
        unsupported_sns = [ch for ch in data.channels if ch in SNS_CHANNELS]
        if unsupported_sns:
            print(f"[CRAWL] SNS 채널 요청 거부: {unsupported_sns}")
            crawl_logger.log_error(
                user_id=user_id,
                input_text=data.input_text,
                channels=data.channels,
                error_type="VALIDATION",
                error_message=f"현재 SNS 채널은 크롤링을 지원하지 않습니다: {unsupported_sns}"
            )
            raise HTTPException(
                status_code=501,
                detail={
                    "message": f"현재 SNS 채널은 크롤링을 지원하지 않습니다: {unsupported_sns}",
                    "supported_community_channels": COMMUNITY_CHANNELS,
                    "note": "SNS 채널 분석은 서비스 준비 중입니다."
                }
            )

        # Validate channels (only community channels supported)
        unsupported_channels = [ch for ch in data.channels if ch not in COMMUNITY_CHANNELS]
        if unsupported_channels:
            print(f"[CRAWL] 미지원 채널 요청 거부: {unsupported_channels}")
            crawl_logger.log_error(
                user_id=user_id,
                input_text=data.input_text,
                channels=data.channels,
                error_type="VALIDATION",
                error_message=f"지원하지 않는 채널이 포함되어 있습니다: {unsupported_channels}"
            )
            raise HTTPException(
                status_code=400,
                detail={
                    "message": f"지원하지 않는 채널이 포함되어 있습니다: {unsupported_channels}",
                    "supported_community_channels": COMMUNITY_CHANNELS,
                    "note": "현재 커뮤니티 채널만 지원됩니다."
                }
            )

        # Generate cache key and check cache
        cache_key = cache_manager.generate_key(data.input_text, data.channels)
        print(f"[CRAWL] 캐시 키: {cache_key}")

        cached_result = cache_manager.get(cache_key)
        if cached_result:
            print(f"[CACHE] 캐시에서 결과 반환됨: key={cache_key}")
            crawl_logger.log_request(
                user_id=user_id,
                input_text=data.input_text,
                channels=data.channels,
                from_cache=True,
                result_count=len(cached_result["results"])
            )
            return CrawlResponse(
                results=cached_result["results"],
                final_credit=cached_result["credit_info"]["final_credit"],
                from_cache=True,
                used_channels=used_channels,
                channel_stats=cached_result["channel_stats"],
                meta=cached_result["metadata"]
            )

        # Process credits
        credit_info = credit_manager.process_request(
            text=data.input_text,
            community_channels=[c for c in data.channels if get_channel_type(c) == "community"],
            sns_channels=[],  # SNS channels not supported yet
            user_id=user_id,
            db_connection=None
        )
        print(f"[CREDIT] 사용자 {user_id}에게 {credit_info['final_credit']} 크레딧 차감")

        # Execute crawlers with error handling
        print(f"[CRAWL] 크롤링 시작: {len(data.channels)}개 채널")
        all_results = []
        failed_channels = []
        channel_stats = {}  # 채널별 결과 개수 통계
        success_count = 0
        failure_count = 0

        for channel in data.channels:
            if channel not in CHANNEL_CRAWLER_MAP:
                print(f"[CRAWL][{channel}] 지원하지 않는 채널")
                crawl_logger.log_failure(
                    user_id=user_id,
                    channel=channel,
                    input_text=data.input_text,
                    error_msg="지원하지 않는 채널",
                    error_type="VALIDATION"
                )
                failed_channels.append(channel)
                channel_stats[channel] = 0
                failure_count += 1
                continue

            try:
                print(f"[CRAWL][{channel}] 크롤링 시작")
                result = await CHANNEL_CRAWLER_MAP[channel](data.input_text)
                
                if isinstance(result, Exception):
                    print(f"[CRAWL][{channel}] 크롤링 실패: {str(result)}")
                    crawl_logger.log_failure(
                        user_id=user_id,
                        channel=channel,
                        input_text=data.input_text,
                        error_msg=str(result),
                        error_type="CRAWL"
                    )
                    failed_channels.append(channel)
                    channel_stats[channel] = 0
                    failure_count += 1
                    continue
                    
                # Ensure each result is a string
                if isinstance(result, list):
                    all_results.extend([str(item) for item in result])
                    channel_stats[channel] = len(result)
                else:
                    all_results.append(str(result))
                    channel_stats[channel] = 1
                    
                print(f"[CRAWL][{channel}] 크롤링 완료: {channel_stats[channel]}개 결과")
                success_count += 1
                
            except Exception as e:
                print(f"[CRAWL][{channel}] 크롤링 실패: {str(e)}")
                crawl_logger.log_failure(
                    user_id=user_id,
                    channel=channel,
                    input_text=data.input_text,
                    error_msg=str(e),
                    error_type="EXCEPTION"
                )
                failed_channels.append(channel)
                channel_stats[channel] = 0
                failure_count += 1
                continue

        # Check if any results were obtained
        if not all_results:
            print(f"[CRAWL] 모든 채널 크롤링 실패: {failed_channels}")
            crawl_logger.log_error(
                user_id=user_id,
                input_text=data.input_text,
                channels=data.channels,
                error_type="SYSTEM",
                error_message="모든 채널 크롤링에 실패했습니다"
            )
            raise HTTPException(
                status_code=500,
                detail="모든 채널 크롤링에 실패했습니다."
            )

        # Log partial success if some channels failed
        if failed_channels:
            print(f"[CRAWL] 일부 채널 크롤링 실패: {failed_channels}")
            print(f"[CRAWL] 성공한 결과 수: {len(all_results)}")

        # 크롤링 결과 취합
        results = []
        for channel, channel_result in zip(data.channels, all_results):
            # 각 결과에 채널 라벨 추가
            labeled_results = []
            for result in channel_result:
                # 제목과 본문에 채널 라벨 추가
                if "title" in result:
                    result["title"] = format_result_with_channel(channel, result["title"])
                if "content" in result:
                    result["content"] = format_result_with_channel(channel, result["content"])
                labeled_results.append(result)
            results.extend(labeled_results)

        print(f"[CRAWL] 채널 라벨 추가 후 결과: {len(results)}개")

        # 중복 제거 로직
        unique_results = []
        seen_contents = set()
        
        for result in results:
            # 본문과 제목을 결합하여 중복 체크
            content_key = f"{result.get('title', '')} {result.get('content', '')}".strip()
            
            # 빈 내용이거나 이미 본 내용이면 건너뛰기
            if not content_key or content_key in seen_contents:
                continue
                
            # 중복되지 않은 결과만 추가
            unique_results.append(result)
            seen_contents.add(content_key)
            
        print(f"[CRAWL] 중복 제거 후 결과: {len(unique_results)}개 (원본: {len(results)}개)")

        # 짧은 문장 필터링
        from ....utils.text_cleaner import filter_short_results
        filtered_results = filter_short_results(unique_results, min_length=10)
        print(f"[CRAWL] 짧은 문장 필터링 후 결과: {len(filtered_results)}개 (중복 제거 후: {len(unique_results)}개)")

        # 최대 결과 개수 제한
        MAX_RESULT_COUNT = 30
        final_results = filtered_results[:MAX_RESULT_COUNT]
        print(f"[CRAWL] 최종 결과 개수: {len(final_results)}개 (최대 {MAX_RESULT_COUNT}개 제한)")

        # Claude 분석을 위한 샘플링 적용
        if len(final_results) > MAX_ANALYSIS_INPUT_COUNT:
            sampled_results = final_results[:MAX_ANALYSIS_INPUT_COUNT]
            was_sampled = True
            print(f"[CRAWL] Claude 분석을 위한 샘플링 적용: {len(final_results)}개 -> {len(sampled_results)}개")
        else:
            sampled_results = final_results
            was_sampled = False

        # 메타데이터 통계 계산
        metadata = calculate_metadata(final_results)
        metadata["was_sampled"] = was_sampled
        metadata["original_count"] = len(final_results)
        metadata["sampled_count"] = len(sampled_results)
        
        # 실패율 계산
        total_attempted = success_count + failure_count
        fail_rate = round((failure_count / total_attempted) * 100, 1) if total_attempted > 0 else 0
        metadata["success_count"] = success_count
        metadata["failure_count"] = failure_count
        metadata["fail_rate_percent"] = fail_rate
        
        print(f"[CRAWL] 메타데이터: 총 {metadata['total_count']}개, 평균 길이 {metadata['average_length']}자, 실패율 {fail_rate}%")

        # 결과 저장
        save_crawl_result(user_id, data.input_text, data.channels, final_results)

        # 분석 이력 기록
        crawl_logger.log_analysis_history(
            user_id=user_id,
            input_text=data.input_text,
            channels=data.channels,
            results=final_results,
            metadata=metadata
        )

        # 캐시에 저장
        cache_manager.set(
            cache_key,
            {
                "results": final_results,
                "credit_info": credit_info,
                "channel_stats": channel_stats,
                "metadata": metadata
            }
        )
        print(f"[CACHE] 캐시 저장 완료: key={cache_key}, 항목 수={len(final_results)}")

        # 최종 결과 반환
        crawl_logger.log_request(
            user_id=user_id,
            input_text=data.input_text,
            channels=data.channels,
            from_cache=False,
            result_count=len(final_results)
        )
        return CrawlResponse(
            from_cache=False,
            final_credit=credit_info["final_credit"],
            used_channels=used_channels,
            results=sampled_results,
            channel_stats=channel_stats,
            meta={
                "total_count": metadata["total_count"],
                "average_length": metadata["average_length"],
                "was_sampled": was_sampled,
                "fail_rate_percent": fail_rate
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"[CRAWL] 시스템 오류 발생: {str(e)}")
        crawl_logger.log_error(
            user_id=user_id,
            input_text=data.input_text,
            channels=data.channels,
            error_type="SYSTEM",
            error_message=str(e)
        )
        raise HTTPException(status_code=500, detail="크롤링 중 오류가 발생했습니다") 