"""
API Key Management Service

This module provides functionality for managing API keys:
- Generating new API keys
- Validating existing keys
- Retrieving user information by API key

The current implementation uses in-memory storage, but the interface
is designed to be easily adapted for database or Redis storage.
"""

from typing import Dict, Optional
import uuid
import os
from datetime import datetime, timedelta

class ApiKeyManager:
    def __init__(self):
        self._api_key_storage: Dict[str, str] = {}  # user_id -> api_key
        self._user_storage: Dict[str, str] = {}  # api_key -> user_id
        self._key_expiry: Dict[str, datetime] = {}  # api_key -> expiry_time

    def generate_api_key(self, user_id: str) -> str:
        """Generate a new API key for a user"""
        if not user_id:
            raise ValueError("User ID cannot be empty")
            
        # Revoke existing key if any
        self.revoke_api_key(user_id)
        
        # Generate new key
        api_key = str(uuid.uuid4())
        self._api_key_storage[user_id] = api_key
        self._user_storage[api_key] = user_id
        self._key_expiry[api_key] = datetime.now() + timedelta(days=30)  # 30-day expiry
        
        return api_key

    def get_api_key(self, user_id: str) -> Optional[str]:
        """Get API key for a user"""
        if not user_id:
            raise ValueError("User ID cannot be empty")
            
        api_key = self._api_key_storage.get(user_id)
        if api_key and self._is_key_valid(api_key):
            return api_key
        return None

    def get_user_id(self, api_key: str) -> Optional[str]:
        """Get user ID for an API key"""
        if not api_key:
            raise ValueError("API key cannot be empty")
            
        if self._is_key_valid(api_key):
            return self._user_storage.get(api_key)
        return None

    def revoke_api_key(self, user_id: str) -> None:
        """Revoke API key for a user"""
        if not user_id:
            raise ValueError("User ID cannot be empty")
            
        api_key = self._api_key_storage.get(user_id)
        if api_key:
            del self._api_key_storage[user_id]
            del self._user_storage[api_key]
            del self._key_expiry[api_key]

    def _is_key_valid(self, api_key: str) -> bool:
        """Check if API key is valid and not expired"""
        expiry = self._key_expiry.get(api_key)
        if not expiry:
            return False
        return datetime.now() < expiry

    def validate_api_key(self, api_key: str) -> bool:
        """Validate an API key"""
        if not api_key:
            return False
        return self._is_key_valid(api_key) and api_key in self._user_storage

# For debugging and testing purposes
def _get_all_keys() -> Dict[str, str]:
    """Get all stored API keys (for testing only)"""
    return dict(_user_to_key)

def _get_all_users() -> Dict[str, str]:
    """Get all stored user mappings (for testing only)"""
    return dict(_user_to_key) 