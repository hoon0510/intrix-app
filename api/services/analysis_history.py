"""
Analysis History Management Service
"""
from typing import Dict, List, Optional
from datetime import datetime
import uuid

class AnalysisHistory:
    def __init__(self):
        # Mock storage using dictionaries
        # analysis_id -> analysis data
        self._analysis_store: Dict[str, Dict] = {}
        
        # user_id -> list of analysis_ids
        self._user_history: Dict[str, List[str]] = {}
        
    def _generate_analysis_id(self) -> str:
        """
        Generate a unique analysis ID
        
        Returns:
            String representing unique analysis ID
        """
        return str(uuid.uuid4())
        
    def _get_timestamp(self) -> str:
        """
        Get current timestamp in ISO format
        
        Returns:
            String representing current timestamp
        """
        return datetime.now().isoformat()
        
    def save_analysis_result(self, user_id: str, data: Dict) -> str:
        """
        Save analysis result and associate it with user
        
        Args:
            user_id: ID of the user
            data: Analysis result data to store
            
        Returns:
            String representing the analysis ID
            
        Note:
            Data structure will be:
            {
                "analysis_id": str,
                "user_id": str,
                "timestamp": str,
                "input_text": str,
                "channels": List[str],
                "result": {
                    "final_credit": int,
                    "free_trial": bool,
                    "copy": str,
                    "report_html": str
                }
            }
        """
        # Generate unique analysis ID
        analysis_id = self._generate_analysis_id()
        
        # Prepare analysis record
        analysis_record = {
            "analysis_id": analysis_id,
            "user_id": user_id,
            "timestamp": self._get_timestamp(),
            **data  # Include all provided data
        }
        
        try:
            # Store analysis record
            self._analysis_store[analysis_id] = analysis_record
            
            # Update user history
            if user_id not in self._user_history:
                self._user_history[user_id] = []
            self._user_history[user_id].append(analysis_id)
            
            return analysis_id
            
        except Exception as e:
            raise ValueError(f"Failed to save analysis result: {str(e)}")
            
    def get_user_history(self, user_id: str) -> List[Dict]:
        """
        Get analysis history for a user
        
        Args:
            user_id: ID of the user
            
        Returns:
            List of analysis records for the user, sorted by timestamp (newest first)
        """
        try:
            # Get list of analysis IDs for user
            analysis_ids = self._user_history.get(user_id, [])
            
            # Get full analysis records
            history = [
                self._analysis_store[aid]
                for aid in analysis_ids
                if aid in self._analysis_store
            ]
            
            # Sort by timestamp (newest first)
            return sorted(
                history,
                key=lambda x: x.get("timestamp", ""),
                reverse=True
            )
            
        except Exception as e:
            raise ValueError(f"Failed to get user history: {str(e)}")
            
    def get_analysis_by_id(self, analysis_id: str) -> Optional[Dict]:
        """
        Get analysis result by ID
        
        Args:
            analysis_id: ID of the analysis to retrieve
            
        Returns:
            Analysis record if found, None otherwise
        """
        try:
            return self._analysis_store.get(analysis_id)
        except Exception as e:
            raise ValueError(f"Failed to get analysis: {str(e)}")
            
    def delete_analysis(self, analysis_id: str, user_id: str) -> bool:
        """
        Delete an analysis record
        
        Args:
            analysis_id: ID of the analysis to delete
            user_id: ID of the user (for verification)
            
        Returns:
            Boolean indicating if deletion was successful
        """
        try:
            # Check if analysis exists and belongs to user
            analysis = self._analysis_store.get(analysis_id)
            if not analysis or analysis.get("user_id") != user_id:
                return False
                
            # Remove from analysis store
            del self._analysis_store[analysis_id]
            
            # Remove from user history
            if user_id in self._user_history:
                self._user_history[user_id].remove(analysis_id)
                
            return True
            
        except Exception:
            return False
            
    def clear_user_history(self, user_id: str) -> bool:
        """
        Clear all analysis history for a user
        
        Args:
            user_id: ID of the user
            
        Returns:
            Boolean indicating if clearing was successful
        """
        try:
            # Get list of analysis IDs for user
            analysis_ids = self._user_history.get(user_id, [])
            
            # Remove all analysis records
            for aid in analysis_ids:
                if aid in self._analysis_store:
                    del self._analysis_store[aid]
                    
            # Clear user history
            self._user_history[user_id] = []
            
            return True
            
        except Exception:
            return False 