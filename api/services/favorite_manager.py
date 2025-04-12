"""
Favorite Manager Service

This module provides functionality for managing user favorites.
Currently implemented with in-memory storage, but designed to be easily
replaced with a database implementation in the future.
"""

from typing import Dict, List, Optional
from fastapi import HTTPException

# In-memory storage for favorites
# Structure: {user_id: [analysis_id1, analysis_id2, ...]}
_favorites_storage: Dict[str, List[str]] = {}

def add_favorite(user_id: str, analysis_id: str) -> None:
    """
    Add an analysis to user's favorites.
    
    Args:
        user_id: ID of the user
        analysis_id: ID of the analysis to favorite
        
    Raises:
        HTTPException: If the analysis is already favorited
    """
    # Initialize user's favorites if not exists
    if user_id not in _favorites_storage:
        _favorites_storage[user_id] = []
    
    # Check if already favorited
    if analysis_id in _favorites_storage[user_id]:
        raise HTTPException(
            status_code=400,
            detail="Analysis is already favorited"
        )
    
    # Add to favorites
    _favorites_storage[user_id].append(analysis_id)

def remove_favorite(user_id: str, analysis_id: str) -> None:
    """
    Remove an analysis from user's favorites.
    
    Args:
        user_id: ID of the user
        analysis_id: ID of the analysis to unfavorite
        
    Raises:
        HTTPException: If the analysis is not favorited
    """
    # Check if user has favorites
    if user_id not in _favorites_storage:
        raise HTTPException(
            status_code=404,
            detail="No favorites found for user"
        )
    
    # Check if analysis is favorited
    if analysis_id not in _favorites_storage[user_id]:
        raise HTTPException(
            status_code=404,
            detail="Analysis is not favorited"
        )
    
    # Remove from favorites
    _favorites_storage[user_id].remove(analysis_id)

def is_favorited(user_id: str, analysis_id: str) -> bool:
    """
    Check if an analysis is favorited by a user.
    
    Args:
        user_id: ID of the user
        analysis_id: ID of the analysis to check
        
    Returns:
        bool: True if favorited, False otherwise
    """
    if user_id not in _favorites_storage:
        return False
    
    return analysis_id in _favorites_storage[user_id]

def get_favorites(user_id: str) -> List[str]:
    """
    Get list of favorited analysis IDs for a user.
    
    Args:
        user_id: ID of the user
        
    Returns:
        List[str]: List of favorited analysis IDs
    """
    return _favorites_storage.get(user_id, [])

# For debugging and testing purposes
def _get_all_favorites() -> Dict[str, List[str]]:
    """
    Get all favorites (for debugging purposes only).
    
    Returns:
        Dict[str, List[str]]: All favorites in the system
    """
    return _favorites_storage.copy()

def _clear_favorites() -> None:
    """
    Clear all favorites (for testing purposes only).
    """
    _favorites_storage.clear() 