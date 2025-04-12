from typing import Dict, Any, Optional, List
import anthropic
from anthropic import Anthropic
import time
from ..config import Config

class ClaudeCaller:
    def __init__(self):
        """Initialize Claude caller with configuration"""
        Config.validate_api_keys()
        self.config = Config.get_claude_config()
        self.client = Anthropic(api_key=self.config["api_key"])
    
    async def call(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Call Claude API with the given parameters
        
        Args:
            prompt: The user's prompt
            system: Optional system message
            temperature: Optional temperature parameter
            max_tokens: Optional max tokens parameter
            timeout: Optional timeout in seconds
            
        Returns:
            Dictionary containing the API response
            
        Raises:
            ValueError: If the API call fails
            TimeoutError: If the API call times out
        """
        try:
            messages: List[Dict[str, str]] = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            response = await self.client.messages.create(
                model=self.config["model"],
                messages=messages,
                temperature=temperature or self.config["temperature"],
                max_tokens=max_tokens or self.config["max_tokens"],
                timeout=timeout or self.config["timeout"]
            )
            
            return {
                "content": response.content[0].text,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "model": response.model
            }
            
        except anthropic.APIError as e:
            raise ValueError(f"Anthropic API error: {str(e)}")
        except anthropic.APITimeoutError as e:
            raise TimeoutError(f"Anthropic API timeout: {str(e)}")
        except anthropic.AuthenticationError as e:
            raise ValueError(f"Anthropic API authentication error: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error in Claude API call: {str(e)}")
    
    async def call_with_retry(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[int] = None,
        max_retries: int = 3,
        retry_delay: int = 1
    ) -> Dict[str, Any]:
        """
        Call Claude API with retry logic
        
        Args:
            prompt: The user's prompt
            system: Optional system message
            temperature: Optional temperature parameter
            max_tokens: Optional max tokens parameter
            timeout: Optional timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            
        Returns:
            Dictionary containing the API response
        """
        for attempt in range(max_retries):
            try:
                return await self.call(
                    prompt=prompt,
                    system=system,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=timeout
                )
            except (ValueError, TimeoutError) as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
        raise ValueError("Maximum retry attempts reached") 