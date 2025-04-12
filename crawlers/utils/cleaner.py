"""
Text Cleaning Utility
"""

import re
import emoji
from typing import List

class TextCleaner:
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean text by removing emojis, URLs, special characters, and extra whitespace
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
            
        # Remove emojis
        text = emoji.replace_emoji(text, '')
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove special characters (non-language symbols)
        # Keep basic punctuation and alphanumeric characters
        text = re.sub(r'[^\w\s.,!?]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
        
    @staticmethod
    def clean_list(texts: List[str]) -> List[str]:
        """
        Clean a list of texts
        
        Args:
            texts: List of texts to clean
            
        Returns:
            List of cleaned texts
        """
        return [TextCleaner.clean_text(text) for text in texts if text] 