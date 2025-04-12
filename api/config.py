import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # API Settings
    OPENAI_MODEL: str = "gpt-4"
    CLAUDE_MODEL: str = "claude-3-sonnet-20240229"
    
    # Default parameters
    DEFAULT_TEMPERATURE: float = 0.7
    DEFAULT_MAX_TOKENS: int = 2000
    DEFAULT_TIMEOUT: int = 30  # seconds
    
    @classmethod
    def validate_api_keys(cls) -> None:
        """Validate that all required API keys are present"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is not set in environment variables")
    
    @classmethod
    def get_openai_config(cls) -> dict:
        """Get OpenAI API configuration"""
        return {
            "api_key": cls.OPENAI_API_KEY,
            "model": cls.OPENAI_MODEL,
            "temperature": cls.DEFAULT_TEMPERATURE,
            "max_tokens": cls.DEFAULT_MAX_TOKENS,
            "timeout": cls.DEFAULT_TIMEOUT
        }
    
    @classmethod
    def get_claude_config(cls) -> dict:
        """Get Claude API configuration"""
        return {
            "api_key": cls.ANTHROPIC_API_KEY,
            "model": cls.CLAUDE_MODEL,
            "temperature": cls.DEFAULT_TEMPERATURE,
            "max_tokens": cls.DEFAULT_MAX_TOKENS,
            "timeout": cls.DEFAULT_TIMEOUT
        } 