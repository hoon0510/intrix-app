"""
Strategy Generation Service using GPT
"""

import json
import os
from typing import Dict, List, Optional
import logging
from api.services.claude_caller import ClaudeCaller
from fastapi import HTTPException

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("uvicorn.access")

class Strategist:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.prompt_dir = os.path.join(os.path.dirname(__file__), "..", "..", "prompts")
        self.claude = ClaudeCaller()
        
    def _load_prompt(self, prompt_type: str) -> str:
        """Load prompt from text file"""
        prompt_path = os.path.join(self.prompt_dir, f"strategy_{prompt_type}.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
            
    async def generate_strategy(self, analysis_result: Dict) -> Dict:
        """
        분석 결과를 바탕으로 마케팅 전략을 생성합니다.
        """
        try:
            logger.info(f"[STRATEGIST] 전략 생성 시작: 분석 결과={analysis_result}")
            
            prompt = f"""
            다음 분석 결과를 바탕으로 마케팅 전략을 생성해주세요:
            {analysis_result}
            
            전략은 다음 항목을 포함해야 합니다:
            1. 타겟 오디언스
            2. 핵심 메시지
            3. 채널 전략
            4. 실행 계획
            """
            
            response = await self.claude.call(
                prompt=prompt,
                system="You are an expert marketing strategist."
            )
            
            if not response or "content" not in response:
                logger.error(f"[STRATEGIST ERROR] Claude 응답 형식 오류: 응답={response}")
                raise Exception("Claude 응답 형식 오류")
            
            logger.info(f"[STRATEGIST] 전략 생성 완료")
            return response["content"]
            
        except Exception as e:
            logger.error(f"[STRATEGIST ERROR] 분석 결과={analysis_result}, 에러={str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="전략 생성 중 오류가 발생했습니다"
            ) 