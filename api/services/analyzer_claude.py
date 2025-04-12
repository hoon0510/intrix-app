"""
Sentiment and Desire Analysis Service using Claude
"""

import json
import os
from typing import Dict, List

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class Analyzer:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.prompt_dir = os.path.join(os.path.dirname(__file__), "..", "..", "prompts")
        
    def _load_prompt(self) -> str:
        """Load analysis prompt from text file"""
        prompt_path = os.path.join(self.prompt_dir, "analysis_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
            
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze text for sentiment and desires using Claude
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        prompt = self._load_prompt()
        
        # Format the prompt with the text to analyze
        formatted_prompt = prompt.format(text=text)
        
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4000,
                messages=[
                    {
                        "role": "user",
                        "content": formatted_prompt
                    }
                ]
            )
            
            # Parse the response into a structured format
            analysis = json.loads(response.content[0].text)
            return analysis
            
        except Exception as e:
            raise Exception(f"Analysis failed: {str(e)}")
            
    def analyze_multiple_texts(self, texts: List[str]) -> Dict:
        """
        Analyze multiple texts and combine the results
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            Dictionary containing combined analysis results
        """
        all_analyses = []
        
        for text in texts:
            analysis = self.analyze_text(text)
            all_analyses.append(analysis)
            
        # Combine analyses (implement your combination logic here)
        combined_analysis = {
            "sentiments": [],
            "desires": [],
            "key_phrases": [],
            "overall_sentiment": "neutral"
        }
        
        for analysis in all_analyses:
            combined_analysis["sentiments"].extend(analysis.get("sentiments", []))
            combined_analysis["desires"].extend(analysis.get("desires", []))
            combined_analysis["key_phrases"].extend(analysis.get("key_phrases", []))
            
        return combined_analysis 