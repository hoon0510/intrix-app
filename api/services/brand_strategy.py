"""
Brand Strategy Generator Module

This module generates brand strategy elements (reference point, frame shift, positioning)
from GPT-generated strategy results using GPT-4.
"""

import json
import os
from typing import Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class BrandStrategyGenerator:
    """Generates brand strategy elements from GPT strategy results."""
    
    def __init__(self):
        """Initialize the BrandStrategyGenerator with OpenAI client."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def _extract_key_elements(self, strategy: Dict) -> Dict:
        """
        Extract key elements from strategy JSON.
        
        Args:
            strategy: Dictionary containing GPT-generated strategy
            
        Returns:
            Dictionary with extracted key elements
        """
        return {
            "core_message": strategy.get("core_message", ""),
            "differentiation": strategy.get("differentiation", ""),
            "target": strategy.get("target", "")
        }
        
    def _generate_brand_strategy(self, key_elements: Dict) -> Dict:
        """
        Generate brand strategy using GPT-4.
        
        Args:
            key_elements: Dictionary containing extracted key elements
            
        Returns:
            Dictionary containing brand strategy elements
        """
        prompt = f"""
        Based on the following marketing strategy elements, generate a brand strategy:
        
        Core Message: {key_elements['core_message']}
        Differentiation: {key_elements['differentiation']}
        Target: {key_elements['target']}
        
        Generate a brand strategy with the following elements:
        1. Reference Point: An existing brand or category that the target audience would associate with
        2. Frame Shift: A strategic perspective that repositions the reference point
        3. Positioning: A one-line positioning statement (slogan or tagline)
        
        Return the response in JSON format with these exact keys:
        {{
            "reference_point": "...",
            "frame_shift": "...",
            "positioning": "..."
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a brand strategy expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse the response
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            raise Exception(f"Failed to generate brand strategy: {str(e)}")
            
    def generate(self, strategy: Dict) -> Dict:
        """
        Generate complete brand strategy from GPT strategy results.
        
        Args:
            strategy: Dictionary containing GPT-generated strategy
            
        Returns:
            Dictionary containing brand strategy elements
            
        Example:
            {
                "reference_point": "갤럭시 S 시리즈",
                "frame_shift": "AI 기능을 강조한 업무 최적화 기기",
                "positioning": "생각보다 빠른, 일보다 똑똑한"
            }
        """
        try:
            # Extract key elements from strategy
            key_elements = self._extract_key_elements(strategy)
            
            # Generate brand strategy
            brand_strategy = self._generate_brand_strategy(key_elements)
            
            return brand_strategy
            
        except Exception as e:
            raise Exception(f"Failed to generate brand strategy: {str(e)}") 