"""
Share link management service for generating and retrieving shareable links.
"""
from typing import Dict, Optional, Tuple
import uuid
from datetime import datetime, timedelta
import os

class ShareLinkManager:
    def __init__(self):
        self._share_link_storage: Dict[str, Tuple[str, str, datetime]] = {}
        self._link_expiry = timedelta(days=7)  # 7-day expiry

    def exists_share_link(self, user_id: str, analysis_id: str) -> bool:
        """Check if a share link already exists for the given user and analysis"""
        if not user_id or not analysis_id:
            raise ValueError("User ID and Analysis ID cannot be empty")
            
        for stored_user_id, stored_analysis_id, created_at in self._share_link_storage.values():
            if (stored_user_id == user_id and 
                stored_analysis_id == analysis_id and 
                self._is_link_valid(created_at)):
                return True
        return False

    def create_share_link(self, user_id: str, analysis_id: str) -> Optional[str]:
        """Create a new share link"""
        if not user_id or not analysis_id:
            raise ValueError("User ID and Analysis ID cannot be empty")
            
        # Check if link already exists
        if self.exists_share_link(user_id, analysis_id):
            return None
            
        # Generate new UUID
        share_uuid = str(uuid.uuid4())
        
        # Store the mapping
        self._share_link_storage[share_uuid] = (
            user_id,
            analysis_id,
            datetime.now()
        )
        
        return share_uuid

    def get_share_info(self, share_uuid: str) -> Optional[Tuple[str, str]]:
        """Get user ID and analysis ID for a share link"""
        if not share_uuid:
            raise ValueError("Share UUID cannot be empty")
            
        if share_uuid not in self._share_link_storage:
            return None
            
        user_id, analysis_id, created_at = self._share_link_storage[share_uuid]
        if not self._is_link_valid(created_at):
            return None
            
        return user_id, analysis_id

    def delete_share_link(self, share_uuid: str) -> bool:
        """Delete a share link"""
        if not share_uuid:
            raise ValueError("Share UUID cannot be empty")
            
        if share_uuid in self._share_link_storage:
            del self._share_link_storage[share_uuid]
            return True
        return False

    def _is_link_valid(self, created_at: datetime) -> bool:
        """Check if a share link is still valid"""
        return datetime.now() - created_at < self._link_expiry

    def cleanup_expired_links(self) -> None:
        """Remove expired share links"""
        current_time = datetime.now()
        expired_uuids = [
            uuid for uuid, (_, _, created_at) in self._share_link_storage.items()
            if current_time - created_at >= self._link_expiry
        ]
        
        for uuid in expired_uuids:
            del self._share_link_storage[uuid]

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

def get_all_share_links() -> Dict[str, Tuple[str, str, datetime]]:
    """
    Get all share links (for debugging purposes).
    
    Returns:
        Dictionary of all share links
    """
    return _share_link_storage.copy() 