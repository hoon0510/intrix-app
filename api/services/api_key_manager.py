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

# In-memory storage for API keys
# Maps user_id to api_key
_user_to_key: Dict[str, str] = {}

# Maps api_key to user_id
_key_to_user: Dict[str, str] = {}

def create_api_key(user_id: str) -> str:
    """
    Generate a new API key for a user and store it.
    
    Args:
        user_id: The user ID to generate the key for
        
    Returns:
        The generated API key
        
    Raises:
        ValueError: If user_id is empty or invalid
    """
    if not user_id or not isinstance(user_id, str):
        raise ValueError("유효하지 않은 사용자 ID입니다")
    
    # Generate a new UUID-based API key
    api_key = str(uuid.uuid4())
    
    # Store the mapping in both directions
    _user_to_key[user_id] = api_key
    _key_to_user[api_key] = user_id
    
    return api_key

def is_valid_api_key(api_key: str) -> bool:
    """
    Check if an API key is valid.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        True if the key is valid, False otherwise
    """
    return api_key in _key_to_user

def get_user_by_api_key(api_key: str) -> Optional[str]:
    """
    Get the user ID associated with an API key.
    
    Args:
        api_key: The API key to look up
        
    Returns:
        The user ID if found, None otherwise
    """
    return _key_to_user.get(api_key)

def revoke_api_key(user_id: str) -> None:
    """
    Revoke an API key for a user.
    
    Args:
        user_id: The user ID whose key should be revoked
    """
    if user_id in _user_to_key:
        api_key = _user_to_key[user_id]
        del _user_to_key[user_id]
        del _key_to_user[api_key]

def get_api_key_by_user(user_id: str) -> Optional[str]:
    """
    Get the API key associated with a user ID.
    
    Args:
        user_id: The user ID to look up
        
    Returns:
        The API key if found, None otherwise
    """
    return _user_to_key.get(user_id)

# For debugging and testing purposes
def _get_all_keys() -> Dict[str, str]:
    """Get all stored API keys (for testing only)"""
    return dict(_key_to_user)

def _get_all_users() -> Dict[str, str]:
    """Get all stored user mappings (for testing only)"""
    return dict(_user_to_key) 