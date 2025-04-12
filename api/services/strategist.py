"""
Strategy Generation Service using GPT
"""

import json
import os
from typing import Dict, List, Optional

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class Strategist:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.prompt_dir = os.path.join(os.path.dirname(__file__), "..", "..", "prompts")
        
    def _load_prompt(self, prompt_type: str) -> str:
        """Load prompt from text file"""
        prompt_path = os.path.join(self.prompt_dir, f"strategy_{prompt_type}.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
            
    def generate_strategy(self, 
                         analysis_result: Dict,
                         prompt_type: str = "existing") -> Dict:
        """
        Generate marketing strategy based on analysis results
        
        Args:
            analysis_result: Dictionary containing analysis results from Claude
            prompt_type: Type of strategy to generate ("existing" or "new")
            
        Returns:
            Dictionary containing the generated strategy
        """
        prompt = self._load_prompt(prompt_type)
        
        # Format the prompt with analysis results
        formatted_prompt = prompt.format(
            analysis=json.dumps(analysis_result, ensure_ascii=False, indent=2)
        )
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a marketing strategy expert."},
                    {"role": "user", "content": formatted_prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            strategy = json.loads(response.choices[0].message.content)
            return strategy
            
        except Exception as e:
            raise Exception(f"Strategy generation failed: {str(e)}") 