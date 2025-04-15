import asyncio
import argparse
from typing import List, Dict, Any
from constants.channel_config import (
    COMMUNITY_CHANNELS,
    SNS_CHANNELS,
    get_channel_label,
    format_result_with_channel
)

# 크롤러 임포트
from services.crawlers.reddit_crawler import crawl_reddit
from services.crawlers.ppomppu_crawler import crawl_ppomppu
from services.crawlers.dcinside_crawler import crawl_dcinside
from services.crawlers.theqoo_crawler import crawl_theqoo
from services.crawlers.ruliweb_crawler import crawl_ruliweb
from services.crawlers.clien_crawler import crawl_clien

# 채널별 크롤러 매핑
CRAWLER_MAP = {
    "reddit": crawl_reddit,
    "ppomppu": crawl_ppomppu,
    "dcinside": crawl_dcinside,
    "theqoo": crawl_theqoo,
    "ruliweb": crawl_ruliweb,
    "clien": crawl_clien
}

def print_result(channel: str, results: List[Dict[str, Any]]) -> None:
    """
    크롤링 결과를 포맷팅하여 출력합니다.
    
    Args:
        channel (str): 채널 키
        results (List[Dict[str, Any]]): 크롤링 결과 리스트
    """
    label = get_channel_label(channel)
    print(f"\n[{label} 크롤링 결과]")
    print(f"총 {len(results)}개 결과")
    print("-" * 50)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. 제목: {result.get('title', '')}")
        print(f"   내용: {result.get('content', '')}")
        if 'url' in result:
            print(f"   URL: {result['url']}")
        print("-" * 50)

async def run_crawler(channel: str, text: str) -> List[Dict[str, Any]]:
    """
    지정된 채널의 크롤러를 실행합니다.
    
    Args:
        channel (str): 채널 키
        text (str): 검색어
        
    Returns:
        List[Dict[str, Any]]: 크롤링 결과
    """
    try:
        crawler_func = CRAWLER_MAP[channel]
        results = await crawler_func(text)
        return results
    except Exception as e:
        print(f"[{channel}] 크롤링 실패: {str(e)}")
        return []

async def main():
    parser = argparse.ArgumentParser(description='크롤러 테스트 CLI')
    parser.add_argument('--text', type=str, help='검색할 텍스트')
    parser.add_argument('--channels', nargs='+', help='크롤링할 채널 목록 (지정하지 않으면 모든 채널)')
    args = parser.parse_args()

    # 검색어 입력
    text = args.text
    if not text:
        text = input("검색어 입력: ")

    # 채널 선택
    available_channels = list(CRAWLER_MAP.keys())
    if args.channels:
        channels = [ch for ch in args.channels if ch in available_channels]
        if not channels:
            print(f"지원하지 않는 채널입니다. 가능한 채널: {', '.join(available_channels)}")
            return
    else:
        print("\n크롤링할 채널을 선택하세요 (여러 개 선택 가능):")
        for i, ch in enumerate(available_channels, 1):
            print(f"{i}. {get_channel_label(ch)}")
        print("0. 모든 채널")
        
        selection = input("\n선택 (쉼표로 구분): ")
        if selection == "0":
            channels = available_channels
        else:
            try:
                indices = [int(x.strip()) - 1 for x in selection.split(",")]
                channels = [available_channels[i] for i in indices if 0 <= i < len(available_channels)]
            except (ValueError, IndexError):
                print("잘못된 입력입니다.")
                return

    # 크롤링 실행
    print(f"\n검색어: {text}")
    print(f"선택된 채널: {', '.join(get_channel_label(ch) for ch in channels)}")
    print("\n크롤링을 시작합니다...")

    for channel in channels:
        results = await run_crawler(channel, text)
        print_result(channel, results)

if __name__ == "__main__":
    asyncio.run(main()) 