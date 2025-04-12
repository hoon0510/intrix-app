"""
Share link management service for generating and retrieving shareable links.
"""
from typing import Dict, Optional, Tuple
import uuid
from datetime import datetime, timedelta

# In-memory storage for share links
# Format: {share_uuid: (user_id, analysis_id, created_at)}
_share_link_storage: Dict[str, Tuple[str, str, datetime]] = {}

# TTL constants (in seconds)
LINK_TTL_SECONDS = 86400  # 24 hours

def exists_share_link(user_id: str, analysis_id: str) -> bool:
    """
    Check if a share link exists for the given user and analysis.
    
    Args:
        user_id: ID of the user
        analysis_id: ID of the analysis
        
    Returns:
        True if a valid share link exists, False otherwise
    """
    if not user_id or not analysis_id:
        return False
        
    # Check for existing valid link
    for stored_user_id, stored_analysis_id, created_at in _share_link_storage.values():
        if stored_user_id == user_id and stored_analysis_id == analysis_id:
            # Check if existing link is still valid
            expiration_time = created_at + timedelta(seconds=LINK_TTL_SECONDS)
            if datetime.now() <= expiration_time:
                return True
            else:
                return False
                
    return False

def create_share_link(user_id: str, analysis_id: str) -> Optional[str]:
    """
    Create a share link for an analysis.
    
    Args:
        user_id: ID of the user creating the share link
        analysis_id: ID of the analysis to share
        
    Returns:
        Share UUID if successful, None otherwise
    """
    if not user_id or not analysis_id:
        return None
        
    # Check for existing valid link
    for share_uuid, (stored_user_id, stored_analysis_id, created_at) in _share_link_storage.items():
        if stored_user_id == user_id and stored_analysis_id == analysis_id:
            # Check if existing link is still valid
            expiration_time = created_at + timedelta(seconds=LINK_TTL_SECONDS)
            if datetime.now() <= expiration_time:
                return share_uuid
            else:
                # Remove expired link
                del _share_link_storage[share_uuid]
                break
        
    # Generate new UUID if no valid existing link found
    share_uuid = str(uuid.uuid4())
    
    # Store with creation timestamp
    _share_link_storage[share_uuid] = (user_id, analysis_id, datetime.now())
    
    return share_uuid

def get_analysis_id_by_uuid(share_uuid: str) -> Optional[str]:
    """
    Get analysis ID from share UUID, checking for expiration.
    
    Args:
        share_uuid: UUID of the share link
        
    Returns:
        Analysis ID if valid and not expired, None otherwise
    """
    if share_uuid not in _share_link_storage:
        return None
        
    user_id, analysis_id, created_at = _share_link_storage[share_uuid]
    
    # Check if link has expired
    expiration_time = created_at + timedelta(seconds=LINK_TTL_SECONDS)
    if datetime.now() > expiration_time:
        return None
        
    return analysis_id

def get_user_id_by_uuid(share_uuid: str) -> Optional[str]:
    """
    Get user ID from share UUID.
    
    Args:
        share_uuid: UUID of the share link
        
    Returns:
        User ID if found, None otherwise
    """
    if share_uuid not in _share_link_storage:
        return None
        
    return _share_link_storage[share_uuid][0]

def delete_share_link(share_uuid: str) -> bool:
    """
    Delete a share link.
    
    Args:
        share_uuid: UUID of the share link to delete
        
    Returns:
        True if deleted, False if not found
    """
    if share_uuid in _share_link_storage:
        del _share_link_storage[share_uuid]
        return True
    return False

def get_all_share_links() -> Dict[str, Tuple[str, str, datetime]]:
    """
    Get all share links (for debugging purposes).
    
    Returns:
        Dictionary of all share links
    """
    return _share_link_storage.copy() 