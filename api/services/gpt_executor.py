import os
import logging
from typing import Tuple
import openai
from openai import AsyncOpenAI

# 로거 설정
logger = logging.getLogger(__name__)

# OpenAI 클라이언트 초기화
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 프롬프트 템플릿
EXECUTION_STRATEGY_PROMPT = """
너는 마케팅 콘텐츠 기획 전문가야. 다음 텍스트를 기반으로 콘텐츠 실행 전략을 3단계로 설계해.
입력 텍스트: "{input_text}"

[출력 포맷 예시]
HOOK: (관심을 끄는 도입부 문장)
FLOW: (본문 내용의 전개 방향)
CTA: (행동을 유도하는 문장)

반드시 출력은 다음과 같이 해:
HOOK: ...
FLOW: ...
CTA: ...
"""

async def generate_execution_strategy(input_text: str) -> Tuple[str, str, str]:
    """
    입력 텍스트를 기반으로 HOOK, FLOW, CTA 실행 전략을 생성합니다.
    
    Args:
        input_text: Claude로 분석된 핵심 욕구 요약 텍스트
        
    Returns:
        Tuple[str, str, str]: (hook, flow, cta) 실행 전략
        
    Raises:
        ValueError: GPT 응답 파싱 실패 시
        Exception: GPT API 호출 실패 시
    """
    try:
        logger.info("Starting execution strategy generation")
        
        # GPT API 호출
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a marketing content strategy expert."},
                {"role": "user", "content": EXECUTION_STRATEGY_PROMPT.format(input_text=input_text)}
            ],
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        logger.info("GPT response received successfully")
        
        # 응답 파싱
        try:
            # 각 섹션을 추출
            sections = {}
            current_section = None
            current_content = []
            
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('HOOK:'):
                    current_section = 'hook'
                    current_content = [line[5:].strip()]
                elif line.startswith('FLOW:'):
                    if current_section:
                        sections[current_section] = '\n'.join(current_content)
                    current_section = 'flow'
                    current_content = [line[5:].strip()]
                elif line.startswith('CTA:'):
                    if current_section:
                        sections[current_section] = '\n'.join(current_content)
                    current_section = 'cta'
                    current_content = [line[4:].strip()]
                elif current_section and line:
                    current_content.append(line)
            
            # 마지막 섹션 저장
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            
            # 필수 섹션 확인
            required_sections = {'hook', 'flow', 'cta'}
            if not all(section in sections for section in required_sections):
                raise ValueError("Missing required sections in GPT response")
            
            logger.info("Successfully parsed GPT response")
            return sections['hook'], sections['flow'], sections['cta']
            
        except Exception as e:
            logger.error(f"Error parsing GPT response: {str(e)}")
            raise ValueError(f"Failed to parse GPT response: {str(e)}")
            
    except Exception as e:
        logger.error(f"Error generating execution strategy: {str(e)}")
        raise Exception(f"Failed to generate execution strategy: {str(e)}") 