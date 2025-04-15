"""
Sentiment and Desire Analysis Service using Claude
"""

import json
import os
from typing import Dict, List, Optional
import logging

from anthropic import Anthropic
from dotenv import load_dotenv
from fastapi import HTTPException
from api.services.claude_caller import ClaudeCaller

load_dotenv()

logger = logging.getLogger("uvicorn.access")

class Analyzer:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.prompt_dir = os.path.join(os.path.dirname(__file__), "..", "..", "prompts")
        self.claude = ClaudeCaller()
        
    def _load_prompt(self) -> str:
        """Load analysis prompt from text file"""
        prompt_path = os.path.join(self.prompt_dir, "analysis_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
            
    async def analyze_text(self, text: str) -> Dict:
        """
        입력 텍스트를 Claude를 사용하여 분석합니다.
        """
        try:
            logger.info(f"[ANALYZER] 텍스트 분석 시작: 길이={len(text)}")
            
            prompt = f"""
            다음 텍스트를 분석해주세요:
            {text}
            
            분석 결과는 다음 형식으로 제공해주세요:
            1. 주요 키워드
            2. 감성 분석
            3. 주요 주제
            4. 인사이트
            """
            
            response = await self.claude.call(
                prompt=prompt,
                system="You are an expert text analyzer."
            )
            
            if not response or "content" not in response:
                logger.error(f"[ANALYZER ERROR] Claude 응답 형식 오류: 응답={response}")
                raise Exception("Claude 응답 형식 오류")
            
            logger.info(f"[ANALYZER] 텍스트 분석 완료")
            return response["content"]
            
        except Exception as e:
            logger.error(f"[ANALYZER ERROR] 입력값={text}, 에러={str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="텍스트 분석 중 오류가 발생했습니다"
            )
            
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