"""
Copy Generation Service
"""

import json
import os
from typing import Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

class Copywriter:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # 욕구 태그별 스타일 매핑
        self.style_mapping = {
            "쾌락추구": "욕망자극형",
            "성공추구": "성공자극형",
            "안전추구": "안심자극형",
            "소속추구": "공감자극형",
            "자존추구": "자부심자극형",
            "호기심추구": "호기심자극형",
            "독립추구": "자유자극형",
            "경쟁추구": "경쟁자극형"
        }
        
        # 스타일별 프롬프트 파일 경로
        self.prompt_dir = os.path.join(os.path.dirname(__file__), "..", "prompts", "copy_styles")
        
    def _load_style_prompt(self, style: str) -> str:
        """
        Load prompt for the specified style
        
        Args:
            style: Copy style name
            
        Returns:
            String containing the prompt
        """
        prompt_file = os.path.join(self.prompt_dir, f"{style}.txt")
        try:
            with open(prompt_file, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise ValueError(f"Prompt file not found for style: {style}")
            
    def _determine_style(self, desire_tags: List[str]) -> str:
        """
        Determine copy style based on desire tags
        
        Args:
            desire_tags: List of desire tags from Claude
            
        Returns:
            String representing the selected style
        """
        # 욕구 태그별 우선순위 설정
        priority = {
            "쾌락추구": 1,
            "성공추구": 2,
            "안전추구": 3,
            "소속추구": 4,
            "자존추구": 5,
            "호기심추구": 6,
            "독립추구": 7,
            "경쟁추구": 8
        }
        
        # 우선순위가 가장 높은 욕구 태그 선택
        selected_tag = min(desire_tags, key=lambda x: priority.get(x, float('inf')))
        return self.style_mapping.get(selected_tag, "욕망자극형")
        
    def generate_copy(self, 
                     strategy: Dict,
                     analysis_result: Dict,
                     style: Optional[str] = None) -> Dict:
        """
        Generate marketing copy based on strategy and analysis
        
        Args:
            strategy: Marketing strategy
            analysis_result: Analysis results from Claude
            style: Optional specific style to use
            
        Returns:
            Dictionary containing the generated copy and style
        """
        try:
            # 욕구 태그 추출
            desire_tags = analysis_result.get("desires", [])
            if not desire_tags:
                raise ValueError("No desire tags found in analysis result")
                
            # 스타일 결정
            selected_style = style if style else self._determine_style(desire_tags)
            
            # 프롬프트 로드
            prompt = self._load_style_prompt(selected_style)
            
            # 프롬프트 포맷팅
            formatted_prompt = prompt.format(
                strategy=json.dumps(strategy, ensure_ascii=False),
                analysis=json.dumps(analysis_result, ensure_ascii=False)
            )
            
            # GPT-4 호출
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional copywriter. Generate short, impactful copy within 20 words. No explanations or emojis."},
                    {"role": "user", "content": formatted_prompt}
                ],
                temperature=0.7,
                max_tokens=50
            )
            
            # 응답 처리
            copy_text = response.choices[0].message.content.strip()
            
            # 20단어 제한 확인
            words = copy_text.split()
            if len(words) > 20:
                copy_text = " ".join(words[:20])
                
            return {
                "style": selected_style,
                "copy": copy_text
            }
            
        except Exception as e:
            raise Exception(f"Copy generation failed: {str(e)}") 