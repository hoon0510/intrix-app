from typing import Dict, Any, Optional, Tuple
import hashlib
import json
import time
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self, ttl_seconds: int = 600):
        """
        캐시 매니저를 초기화합니다.
        
        Args:
            ttl_seconds (int): 캐시 유효 시간 (초 단위, 기본값: 600초 = 10분)
        """
        self._cache_store: Dict[str, Tuple[Any, float]] = {}
        self.ttl_seconds = ttl_seconds
        self._default_ttl = timedelta(hours=24)  # Default cache duration: 24 hours

    def generate_key(self, input_text: str, channels: list[str]) -> str:
        """
        입력 텍스트와 채널 목록으로 캐시 키를 생성합니다.
        
        Args:
            input_text (str): 검색어
            channels (list[str]): 채널 목록
            
        Returns:
            str: 생성된 캐시 키
        """
        # 입력값 정규화
        normalized_input = input_text.strip().lower()
        normalized_channels = sorted([ch.strip().lower() for ch in channels])
        
        # 키 생성용 문자열 조합
        key_string = f"{normalized_input}:{':'.join(normalized_channels)}"
        
        # SHA-256 해시 생성
        return hashlib.sha256(key_string.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """
        캐시에서 값을 조회합니다.
        
        Args:
            key (str): 캐시 키
            
        Returns:
            Optional[Any]: 캐시된 값 또는 None
        """
        item = self._cache_store.get(key)
        if not item:
            return None
            
        value, timestamp = item
        current_time = time.time()
        
        # TTL 체크
        if current_time - timestamp > self.ttl_seconds:
            print(f"[CACHE] 캐시 만료: key={key}")
            del self._cache_store[key]  # 만료된 항목 제거
            return None
            
        print(f"[CACHE] 캐시 히트: key={key}")
        return value

    def set(self, key: str, value: Any) -> None:
        """
        캐시에 값을 저장합니다.
        
        Args:
            key (str): 캐시 키
            value (Any): 저장할 값
        """
        current_time = time.time()
        self._cache_store[key] = (value, current_time)
        print(f"[CACHE] 캐시 저장: key={key}")

    def clear(self) -> None:
        """캐시를 모두 비웁니다."""
        self._cache_store.clear()
        print("[CACHE] 캐시 초기화")

    def cleanup_expired(self) -> None:
        """
        만료된 캐시 항목을 정리합니다.
        """
        current_time = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self._cache_store.items()
            if current_time - timestamp > self.ttl_seconds
        ]
        
        for key in expired_keys:
            del self._cache_store[key]
            
        if expired_keys:
            print(f"[CACHE] 만료된 항목 {len(expired_keys)}개 정리 완료")

    def _is_expired(self, cache_entry: Dict[str, Any]) -> bool:
        """
        Check if a cache entry is expired
        
        Args:
            cache_entry: Cache entry to check
            
        Returns:
            Boolean indicating if entry is expired
        """
        return datetime.now() > cache_entry["expires_at"]

# Create a singleton instance
cache_manager = CacheManager() 