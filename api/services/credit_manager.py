"""
Credit Management Service
"""

import math
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from .auth_manager import AuthManager, UserRole
from .cache_manager import cache_manager
from ..constants.channel_config import (
    COMMUNITY_CHANNELS,
    SNS_CHANNELS,
    get_channel_type
)
from fastapi import HTTPException

class CreditManager:
    def __init__(self):
        self.base_rate = 100  # 100 bytes = 1 credit
        self.community_multiplier = 0.1  # 10% of base credits
        self.sns_multiplier = 0.2  # 20% of base credits
        self.cache_duration = timedelta(hours=24)  # Cache duration
        self.auth_manager = AuthManager()
        self._user_credits: Dict[str, int] = {}
        self._credit_history: Dict[str, List[Dict]] = {}
        
    def _generate_cache_key(self, text: str, channels: List[str]) -> str:
        """
        Generate cache key from text and channels
        
        Args:
            text: Input text
            channels: List of selected channels
            
        Returns:
            String representing the cache key
        """
        # Sort channels for consistent key generation
        sorted_channels = sorted(channels)
        
        # Create string representation of channels
        channels_str = ",".join(sorted_channels)
        
        # Generate hash of text
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        # Combine text hash and channels
        return f"{text_hash}:{channels_str}"
        
    def calculate_base_credits(self, text_size: int) -> int:
        """
        Calculate base credits based on text size
        
        Args:
            text_size: Size of text in bytes
            
        Returns:
            Integer representing base credits
        """
        return math.ceil(text_size / self.base_rate)
        
    def calculate_channel_credits(self, 
                                base_credits: int,
                                community_channels: List[str],
                                sns_channels: List[str]) -> int:
        """
        Calculate additional credits for selected channels
        
        Args:
            base_credits: Base credits calculated from text size
            community_channels: List of selected community channels
            sns_channels: List of selected SNS channels
            
        Returns:
            Integer representing total credits including channel multipliers
        """
        # Calculate channel-specific credits
        community_credits = len(community_channels) * (base_credits * self.community_multiplier)
        sns_credits = len(sns_channels) * (base_credits * self.sns_multiplier)
        
        total_credits = base_credits + community_credits + sns_credits
        return math.ceil(total_credits)
        
    def calculate_total_credits(self,
                              text_size: int,
                              community_channels: List[str],
                              sns_channels: List[str]) -> int:
        """
        Calculate total credits needed for a request
        
        Args:
            text_size: Size of text in bytes
            community_channels: List of selected community channels
            sns_channels: List of selected SNS channels
            
        Returns:
            Integer representing total credits needed
        """
        base_credits = self.calculate_base_credits(text_size)
        return self.calculate_channel_credits(base_credits, community_channels, sns_channels)
        
    def check_credits(self, 
                     user_id: str,
                     required_credits: int,
                     db_connection) -> bool:
        """
        Check if user has enough credits
        
        Args:
            user_id: ID of the user
            required_credits: Credits needed for the operation
            db_connection: Database connection object
            
        Returns:
            Boolean indicating if user has enough credits
        """
        # Implement database query to check user's credits
        # This is a placeholder - implement your actual database logic
        user_credits = db_connection.get_user_credits(user_id)
        return user_credits >= required_credits
        
    def deduct_credits(self,
                      user_id: str,
                      credits: int,
                      db_connection) -> bool:
        """
        Deduct credits from user's balance
        
        Args:
            user_id: ID of the user
            credits: Credits to deduct
            db_connection: Database connection object
            
        Returns:
            Boolean indicating if deduction was successful
        """
        # Implement database query to deduct credits
        # This is a placeholder - implement your actual database logic
        try:
            db_connection.deduct_credits(user_id, credits)
            return True
        except Exception:
            return False
            
    def check_cache(self,
                   cache_key: str,
                   db_connection) -> Optional[Dict]:
        """
        Check if result exists in cache
        
        Args:
            cache_key: Key to check in cache
            db_connection: Database connection object
            
        Returns:
            Cached result if exists and not expired, None otherwise
        """
        try:
            cached_result = db_connection.get_cache(cache_key)
            if cached_result:
                # Check if cache is still valid
                cache_time = cached_result.get("timestamp")
                if cache_time and datetime.fromisoformat(cache_time) + self.cache_duration > datetime.now():
                    return cached_result.get("data")
            return None
        except Exception:
            return None
            
    def store_cache(self,
                   cache_key: str,
                   data: Dict,
                   db_connection) -> bool:
        """
        Store result in cache
        
        Args:
            cache_key: Key to store in cache
            data: Data to cache
            db_connection: Database connection object
            
        Returns:
            Boolean indicating if caching was successful
        """
        try:
            cache_data = {
                "data": data,
                "timestamp": datetime.now().isoformat()
            }
            db_connection.store_cache(cache_key, cache_data)
            return True
        except Exception:
            return False
            
    def is_eligible_for_free_trial(self, user_id: Optional[str], ip_address: Optional[str], db_connection) -> bool:
        """
        Check if user is eligible for free trial
        
        Args:
            user_id: Optional user ID
            ip_address: Optional IP address
            db_connection: Database connection object
            
        Returns:
            Boolean indicating if user is eligible for free trial
        """
        try:
            if user_id:
                # Check if user has any previous analysis requests
                has_previous_requests = db_connection.has_user_analysis_requests(user_id)
                return not has_previous_requests
            elif ip_address:
                # Check if IP has any analysis requests today
                has_today_requests = db_connection.has_ip_analysis_requests_today(ip_address)
                return not has_today_requests
            return False
        except Exception:
            return False

    def _check_privileged_role(self, user_id: str) -> bool:
        """
        Check if user has a privileged role (admin, tester, partner)
        
        Args:
            user_id: User ID
            
        Returns:
            Boolean indicating if user has a privileged role
        """
        role = self.auth_manager.get_user_role(user_id)
        return role in [UserRole.ADMIN, UserRole.TESTER, UserRole.PARTNER]

    def calculate_credit(self, input_text: str, channels: List[str]) -> Dict[str, int]:
        """
        Calculate required credits for a request
        
        Args:
            input_text: Input text to analyze
            channels: List of channels to crawl
            
        Returns:
            Dict containing:
            - base_credit: Base credit for text length
            - additional_credit: Additional credit for channels
            - total_credit: Total required credit
        """
        # Calculate base credit based on text length
        base_credit = math.ceil(len(input_text.encode("utf-8")) / 100)
        
        # Calculate additional credit for channels
        additional_credit = 0
        for channel in channels:
            if channel in COMMUNITY_CHANNELS:
                additional_credit += base_credit * 0.1
            elif channel in SNS_CHANNELS:
                additional_credit += base_credit * 0.2
        
        total_credit = math.ceil(base_credit + additional_credit)
        
        return {
            "base_credit": base_credit,
            "additional_credit": math.ceil(additional_credit),
            "total_credit": total_credit
        }

    def deduct_credit(self, user_id: str, amount: int) -> Dict[str, int]:
        """
        Deduct credits from user's balance
        
        Args:
            user_id: User ID
            amount: Amount of credits to deduct
            
        Returns:
            Dict containing:
            - deducted_amount: Amount of credits deducted
            - remaining_balance: User's remaining credit balance
        """
        if not self.has_sufficient_credit(user_id, amount):
            raise HTTPException(
                status_code=402,
                detail=f"크레딧이 부족합니다. 필요: {amount}, 보유: {self._user_credits[user_id]}"
            )
            
        self._user_credits[user_id] -= amount
        
        # Record credit history
        if user_id not in self._credit_history:
            self._credit_history[user_id] = []
        self._credit_history[user_id].append({
            "amount": -amount,
            "type": "deduction",
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "deducted_amount": amount,
            "remaining_balance": self._user_credits[user_id]
        }

    def process_request(self, text: str, community_channels: List[str], sns_channels: List[str], user_id: str, db_connection: Optional[Any] = None) -> Dict[str, Any]:
        """
        Process a request and deduct credits
        
        Args:
            text: Input text
            community_channels: List of community channels
            sns_channels: List of social media channels
            user_id: User ID
            db_connection: Optional database connection
            
        Returns:
            Dict containing:
            - credit_info: Credit calculation details
            - deduction_info: Credit deduction details
            - final_credit: Final credit amount deducted
        """
        # Calculate required credits
        credit_info = self.calculate_credit(text, community_channels + sns_channels)
        
        try:
            # Deduct credits
            deduction_info = self.deduct_credit(user_id, credit_info["total_credit"])
            
            return {
                "credit_info": credit_info,
                "deduction_info": deduction_info,
                "final_credit": credit_info["total_credit"]
            }
            
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"크레딧 처리 중 오류 발생: {str(e)}")

    def add_credits(self, user_id: str, amount: int) -> None:
        """
        Add credits to a user's balance
        
        Args:
            user_id: ID of the user
            amount: Amount of credits to add
        """
        if user_id not in self._user_credits:
            self._user_credits[user_id] = 0
        self._user_credits[user_id] += amount

    def deduct_credits(self, user_id: str, amount: int) -> None:
        """
        Deduct credits from a user's balance
        
        Args:
            user_id: ID of the user
            amount: Amount of credits to deduct
        """
        if user_id not in self._user_credits:
            raise ValueError("사용자를 찾을 수 없습니다")
        if self._user_credits[user_id] < amount:
            raise ValueError("크레딧이 부족합니다")
        self._user_credits[user_id] -= amount

    def get_credits(self, user_id: str) -> int:
        """
        Get a user's current credit balance
        
        Args:
            user_id: ID of the user
            
        Returns:
            Current credit balance
        """
        return self._user_credits.get(user_id, 0)

    def has_sufficient_credit(self, user_id: str, amount: int) -> bool:
        """
        Check if user has sufficient credits
        
        Args:
            user_id: User ID
            amount: Required amount of credits
            
        Returns:
            Boolean indicating if user has sufficient credits
        """
        if user_id not in self._user_credits:
            self._user_credits[user_id] = 1000  # Default starting credits
        return self._user_credits[user_id] >= amount

# Global credit manager instance
credit_manager = CreditManager() 