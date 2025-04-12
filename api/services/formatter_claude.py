"""
Report Formatting Service using Claude
"""

import json
import os
from typing import Dict, Optional

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class Formatter:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.prompt_dir = os.path.join(os.path.dirname(__file__), "..", "..", "prompts")
        
    def _load_prompt(self) -> str:
        """Load formatting prompt from text file"""
        prompt_path = os.path.join(self.prompt_dir, "formatting_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
            
    def _validate_strategy(self, strategy: Dict) -> bool:
        """
        Validate strategy structure
        
        Args:
            strategy: Strategy data to validate
            
        Returns:
            Boolean indicating if strategy is valid
        """
        required_fields = [
            "overview",
            "target_audience",
            "key_messages",
            "channels",
            "timeline"
        ]
        
        missing_fields = [field for field in required_fields if field not in strategy]
        if missing_fields:
            print(f"Warning: Missing required fields in strategy: {', '.join(missing_fields)}")
            return False
        return True
        
    def format_report(self, strategy: Dict) -> str:
        """
        Format strategy into HTML report
        
        Args:
            strategy: Strategy data to format
            
        Returns:
            String containing HTML formatted report
        """
        try:
            # Validate strategy structure
            if not self._validate_strategy(strategy):
                print("Warning: Proceeding with incomplete strategy data")
                
            # Prepare prompt
            prompt = f"""다음 전략 데이터를 전문 리포트처럼 HTML로 정리해줘.
각 섹션은 <h2> 태그로 제목을 표시하고, 내용은 <p> 태그로 감싸줘.
전략 데이터:
{json.dumps(strategy, ensure_ascii=False, indent=2)}
"""
            
            # Call Claude API
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract and clean HTML
            html_content = response.content[0].text.strip()
            
            # Ensure proper HTML structure
            if not html_content.startswith("<h2>"):
                html_content = f"<h2>전략 개요</h2>\n<p>{html_content}</p>"
                
            return html_content
            
        except Exception as e:
            raise Exception(f"Report formatting failed: {str(e)}")
            
    def generate_html(self, strategy: Dict) -> str:
        """
        Generate complete HTML document from strategy
        
        Args:
            strategy: Strategy data to format
            
        Returns:
            String containing complete HTML document
        """
        # Format the report content
        content = self.format_report(strategy)
        
        # Create complete HTML document
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>마케팅 전략 보고서</title>
    <style>
        body {{
            font-family: 'Noto Sans KR', sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h2 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-top: 30px;
        }}
        p {{
            color: #34495e;
            margin: 15px 0;
        }}
    </style>
</head>
<body>
    <h1>마케팅 전략 보고서</h1>
    {content}
</body>
</html>"""
        
        return html 