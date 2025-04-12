"""
Credit Management Service
"""

import math
import hashlib
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from .auth_manager import AuthManager, UserRole

class CreditManager:
    def __init__(self):
        self.base_rate = 100  # 100 bytes = 1 credit
        self.community_multiplier = 0.1  # 10% of base credits
        self.sns_multiplier = 0.2  # 20% of base credits
        self.cache_duration = timedelta(hours=24)  # Cache duration
        self.auth_manager = AuthManager()
        
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

    def process_request(self,
                       text: str,
                       community_channels: List[str],
                       sns_channels: List[str],
                       user_id: Optional[str],
                       ip_address: Optional[str],
                       db_connection) -> Dict:
        """
        Process a request with credit calculation and cache checking
        
        Args:
            text: Input text
            community_channels: List of selected community channels
            sns_channels: List of selected SNS channels
            user_id: Optional user ID
            ip_address: Optional IP address
            db_connection: Database connection object
            
        Returns:
            Dictionary containing credit information and cache status
        """
        # Generate cache key
        all_channels = community_channels + sns_channels
        cache_key = self._generate_cache_key(text, all_channels)
        
        # Check cache first
        cached_result = self.check_cache(cache_key, db_connection)
        if cached_result:
            return {
                "final_credit": cached_result.get("final_credit", 0),
                "from_cache": True,
                "free_trial": cached_result.get("free_trial", False)
            }
            
        # Check privileged roles first (admin, tester, partner)
        if user_id and self._check_privileged_role(user_id):
            return {
                "final_credit": 0,
                "from_cache": False,
                "free_trial": True
            }
            
        # For regular members, check free trial eligibility
        is_free_trial = self.is_eligible_for_free_trial(user_id, ip_address, db_connection)
        
        if is_free_trial:
            return {
                "final_credit": 0,
                "from_cache": False,
                "free_trial": True
            }
            
        # Calculate required credits for regular members
        text_size = len(text.encode('utf-8'))
        required_credits = self.calculate_total_credits(
            text_size,
            community_channels,
            sns_channels
        )
        
        # If user_id is provided, check and deduct credits
        if user_id:
            if not self.check_credits(user_id, required_credits, db_connection):
                raise ValueError(f"Insufficient credits. Required: {required_credits}")
            self.deduct_credits(user_id, required_credits, db_connection)
        
        # Store result in cache
        result = {
            "final_credit": required_credits,
            "from_cache": False,
            "free_trial": False
        }
        self.store_cache(cache_key, result, db_connection)
        
        return result 