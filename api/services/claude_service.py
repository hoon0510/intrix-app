# 📁 api/services/claude_service.py

import os
from typing import Dict, Any
import requests
import json

# Claude API 키 및 엔드포인트
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

def load_prompt(prompt_path: str) -> str:
    """Load prompt from file"""
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()

class ClaudeService:
    def __init__(self):
        self.prompt_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
        self.analysis_prompt = load_prompt(os.path.join(self.prompt_dir, "prompt_claude_analysis.txt"))
        self.formatting_prompt = load_prompt(os.path.join(self.prompt_dir, "prompt_claude_formatter.txt"))

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text using Claude API"""
        headers = {
            "Content-Type": "application/json",
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-3-opus-20240229",
            "max_tokens": 4000,
            "messages": [
                {
                    "role": "user",
                    "content": f"{self.analysis_prompt}\n\nText to analyze:\n{text}"
                }
            ]
        }
        
        response = requests.post(CLAUDE_API_URL, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()

    def format_text(self, text: str, style: str) -> Dict[str, Any]:
        """Format text using Claude API"""
        headers = {
            "Content-Type": "application/json",
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-3-opus-20240229",
            "max_tokens": 4000,
            "messages": [
                {
                    "role": "user",
                    "content": f"{self.formatting_prompt}\n\nStyle: {style}\n\nText to format:\n{text}"
                }
            ]
        }
        
        response = requests.post(CLAUDE_API_URL, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()
