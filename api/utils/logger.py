import os
from datetime import datetime
from typing import List, Dict, Any
import json

class CrawlLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self.request_log = os.path.join(log_dir, "crawl_requests.log")
        self.error_log = os.path.join(log_dir, "crawl_errors.log")
        self.failure_log = os.path.join(log_dir, "failed_crawls.log")
        self.analysis_history = os.path.join(log_dir, "analysis_history.jsonl")
        os.makedirs(log_dir, exist_ok=True)

    def log_request(self, user_id: str, input_text: str, channels: List[str], 
                   from_cache: bool = False, result_count: int = 0) -> None:
        """
        크롤링 요청 로그를 기록합니다.
        
        Args:
            user_id (str): 사용자 ID
            input_text (str): 검색어
            channels (List[str]): 요청된 채널 목록
            from_cache (bool): 캐시 사용 여부
            result_count (int): 결과 개수
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cache_status = "CACHE" if from_cache else "NEW"
        
        log_line = (
            f"[{timestamp}] {cache_status} | "
            f"USER={user_id} | "
            f"CHANNELS={','.join(channels)} | "
            f"COUNT={result_count} | "
            f"INPUT={input_text}\n"
        )
        
        with open(self.request_log, "a", encoding="utf-8") as f:
            f.write(log_line)

    def log_error(self, user_id: str, input_text: str, channels: List[str], 
                 error_type: str, error_message: str) -> None:
        """
        크롤링 오류 로그를 기록합니다.
        
        Args:
            user_id (str): 사용자 ID
            input_text (str): 검색어
            channels (List[str]): 요청된 채널 목록
            error_type (str): 오류 유형
            error_message (str): 오류 메시지
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_line = (
            f"[{timestamp}] ERROR | "
            f"USER={user_id} | "
            f"CHANNELS={','.join(channels)} | "
            f"TYPE={error_type} | "
            f"MESSAGE={error_message} | "
            f"INPUT={input_text}\n"
        )
        
        with open(self.error_log, "a", encoding="utf-8") as f:
            f.write(log_line)

    def log_failure(self, user_id: str, channel: str, input_text: str, 
                   error_msg: str, error_type: str = "CRAWL") -> None:
        """
        크롤링 실패 로그를 기록합니다.
        
        Args:
            user_id (str): 사용자 ID
            channel (str): 실패한 채널
            input_text (str): 검색어
            error_msg (str): 오류 메시지
            error_type (str): 오류 유형 (기본값: "CRAWL")
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_line = (
            f"[{timestamp}] {error_type} | "
            f"USER={user_id} | "
            f"CHANNEL={channel} | "
            f"INPUT={input_text} | "
            f"ERROR={error_msg}\n"
        )
        
        with open(self.failure_log, "a", encoding="utf-8") as f:
            f.write(log_line)

    def log_analysis_history(self, user_id: str, input_text: str, channels: List[str], 
                           results: List[Dict[str, Any]], metadata: Dict[str, Any]) -> None:
        """
        분석 이력을 JSONL 형식으로 기록합니다.
        
        Args:
            user_id (str): 사용자 ID
            input_text (str): 검색어
            channels (List[str]): 사용된 채널 목록
            results (List[Dict[str, Any]]): 크롤링 결과
            metadata (Dict[str, Any]): 메타데이터
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 채널별 결과 개수 계산
        channel_counts = {
            channel: sum(1 for result in results 
                        if result.get("channel", "").lower() == channel.lower())
            for channel in channels
        }
        
        entry = {
            "timestamp": timestamp,
            "user_id": user_id,
            "input_text": input_text,
            "channels": channels,
            "channel_counts": channel_counts,
            "total_results": len(results),
            "metadata": {
                "was_sampled": metadata.get("was_sampled", False),
                "original_count": metadata.get("original_count", len(results)),
                "sampled_count": metadata.get("sampled_count", len(results)),
                "average_length": metadata.get("average_length", 0)
            }
        }
        
        with open(self.analysis_history, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            
        print(f"[ANALYSIS] 이력 기록 완료: 사용자={user_id}, 결과={len(results)}개")

# 전역 로거 인스턴스 생성
crawl_logger = CrawlLogger() 