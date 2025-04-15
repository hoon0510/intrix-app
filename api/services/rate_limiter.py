import time
from collections import defaultdict
from typing import Dict, List
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, request_limit: int = 100, window_seconds: int = 86400):
        """
        요청 제한을 관리하는 RateLimiter를 초기화합니다.
        
        Args:
            request_limit (int): 시간 창 내 최대 요청 수 (기본값: 100)
            window_seconds (int): 시간 창 길이 (초 단위, 기본값: 86400 = 24시간)
        """
        self.request_limit = request_limit
        self.window_seconds = window_seconds
        self._user_request_log: Dict[str, List[float]] = defaultdict(list)
        self._user_limits: Dict[str, int] = {}  # 사용자별 커스텀 제한

    def set_user_limit(self, user_id: str, limit: int) -> None:
        """
        특정 사용자의 요청 제한을 설정합니다.
        
        Args:
            user_id (str): 사용자 ID
            limit (int): 새로운 요청 제한
        """
        self._user_limits[user_id] = limit

    def get_user_limit(self, user_id: str) -> int:
        """
        사용자의 요청 제한을 반환합니다.
        
        Args:
            user_id (str): 사용자 ID
            
        Returns:
            int: 사용자의 요청 제한
        """
        return self._user_limits.get(user_id, self.request_limit)

    def check_rate_limit(self, user_id: str) -> None:
        """
        사용자의 요청 제한을 확인합니다.
        
        Args:
            user_id (str): 사용자 ID
            
        Raises:
            Exception: 요청 제한 초과 시
        """
        now = time.time()
        requests = self._user_request_log[user_id]
        user_limit = self.get_user_limit(user_id)

        # 과거 기록 중 유효 시간 내 요청만 남김
        valid_requests = [r for r in requests if now - r < self.window_seconds]
        self._user_request_log[user_id] = valid_requests

        if len(valid_requests) >= user_limit:
            # 다음 요청 가능 시간 계산
            next_request_time = valid_requests[0] + self.window_seconds
            wait_seconds = int(next_request_time - now)
            wait_hours = wait_seconds // 3600
            wait_minutes = (wait_seconds % 3600) // 60
            
            raise Exception(
                f"일일 요청 제한({user_limit}회)을 초과했습니다. "
                f"{wait_hours}시간 {wait_minutes}분 후에 다시 시도해주세요."
            )

        # 새로운 요청 기록
        self._user_request_log[user_id].append(now)

    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """
        사용자의 요청 통계를 반환합니다.
        
        Args:
            user_id (str): 사용자 ID
            
        Returns:
            Dict[str, Any]: 요청 통계 정보
        """
        now = time.time()
        requests = self._user_request_log[user_id]
        user_limit = self.get_user_limit(user_id)

        # 유효 시간 내 요청만 필터링
        valid_requests = [r for r in requests if now - r < self.window_seconds]
        
        return {
            "current_requests": len(valid_requests),
            "request_limit": user_limit,
            "remaining_requests": user_limit - len(valid_requests),
            "window_seconds": self.window_seconds,
            "reset_time": datetime.fromtimestamp(valid_requests[0] + self.window_seconds) if valid_requests else None
        }

# 전역 RateLimiter 인스턴스 생성
rate_limiter = RateLimiter() 