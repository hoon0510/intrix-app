"""
Rate limiting service for ZIP file downloads.
Currently uses in-memory storage but designed to be easily swapped with Redis.
"""

from typing import Dict, Optional
import time

# In-memory storage for download timestamps
_download_timestamps: Dict[str, float] = {}

# Cooldown period in seconds (10 minutes)
DOWNLOAD_COOLDOWN = 600

def record_download_time(user_id: str) -> None:
    """
    Record the current timestamp for a user's download.
    
    Args:
        user_id: The ID of the user who downloaded
    """
    _download_timestamps[user_id] = time.time()

def is_download_allowed(user_id: str) -> bool:
    """
    Check if a user is allowed to download based on cooldown period.
    
    Args:
        user_id: The ID of the user to check
        
    Returns:
        bool: True if download is allowed, False if still in cooldown
    """
    last_download = _download_timestamps.get(user_id)
    if not last_download:
        return True
        
    return time.time() - last_download >= DOWNLOAD_COOLDOWN

def get_remaining_cooldown(user_id: str) -> Optional[int]:
    """
    Get the remaining cooldown time in seconds for a user.
    
    Args:
        user_id: The ID of the user to check
        
    Returns:
        Optional[int]: Remaining cooldown time in seconds, or None if no cooldown
    """
    last_download = _download_timestamps.get(user_id)
    if not last_download:
        return None
        
    remaining = DOWNLOAD_COOLDOWN - (time.time() - last_download)
    return max(0, int(remaining)) if remaining > 0 else None

def clear_download_history(user_id: str) -> None:
    """
    Clear the download history for a user.
    
    Args:
        user_id: The ID of the user to clear
    """
    _download_timestamps.pop(user_id, None)

def get_all_download_timestamps() -> Dict[str, float]:
    """
    Get all download timestamps (for debugging/monitoring).
    
    Returns:
        Dict[str, float]: All user download timestamps
    """
    return _download_timestamps.copy() 