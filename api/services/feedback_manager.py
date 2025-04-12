from typing import Dict, List, Optional, TypedDict
from datetime import datetime

class FeedbackEntry(TypedDict):
    user_id: str
    analysis_id: str
    feedback: str
    timestamp: str

# In-memory storage for feedback
_feedback_storage: Dict[str, List[FeedbackEntry]] = {}

def submit_feedback(user_id: str, analysis_id: str, feedback: str) -> None:
    """
    Submit feedback for an analysis.
    
    Args:
        user_id: ID of the user submitting feedback
        analysis_id: ID of the analysis being rated
        feedback: Either "positive" or "negative"
    
    Raises:
        ValueError: If feedback is not "positive" or "negative"
    """
    if feedback not in ["positive", "negative"]:
        raise ValueError("Feedback must be either 'positive' or 'negative'")
    
    # Create feedback entry
    entry: FeedbackEntry = {
        "user_id": user_id,
        "analysis_id": analysis_id,
        "feedback": feedback,
        "timestamp": datetime.now().isoformat()
    }
    
    # Initialize user's feedback list if not exists
    if user_id not in _feedback_storage:
        _feedback_storage[user_id] = []
    
    # Add feedback to storage
    _feedback_storage[user_id].append(entry)

def get_feedback_summary(analysis_id: str) -> Dict[str, int]:
    """
    Get summary of feedback for an analysis.
    
    Args:
        analysis_id: ID of the analysis
    
    Returns:
        Dictionary with counts of positive and negative feedback
    """
    positive_count = 0
    negative_count = 0
    
    # Count feedback across all users
    for user_feedback in _feedback_storage.values():
        for entry in user_feedback:
            if entry["analysis_id"] == analysis_id:
                if entry["feedback"] == "positive":
                    positive_count += 1
                else:
                    negative_count += 1
    
    return {
        "positive": positive_count,
        "negative": negative_count
    }

def get_user_feedback(user_id: str) -> List[FeedbackEntry]:
    """
    Get all feedback submitted by a user.
    
    Args:
        user_id: ID of the user
    
    Returns:
        List of feedback entries submitted by the user
    """
    return _feedback_storage.get(user_id, [])

def get_analysis_feedback(analysis_id: str) -> List[FeedbackEntry]:
    """
    Get all feedback for a specific analysis.
    
    Args:
        analysis_id: ID of the analysis
    
    Returns:
        List of all feedback entries for the analysis
    """
    feedback_list: List[FeedbackEntry] = []
    
    # Collect feedback from all users
    for user_feedback in _feedback_storage.values():
        for entry in user_feedback:
            if entry["analysis_id"] == analysis_id:
                feedback_list.append(entry)
    
    return feedback_list

def clear_feedback(user_id: str) -> None:
    """
    Clear all feedback for a user.
    
    Args:
        user_id: ID of the user
    """
    if user_id in _feedback_storage:
        del _feedback_storage[user_id] 