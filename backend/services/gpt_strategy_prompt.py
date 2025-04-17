from typing import Dict, Any
import json

def generate_gpt_strategy_prompt(claude_analysis: str, input_data: Dict[str, Any]) -> str:
    """
    Claude의 감정/욕구 분석 결과를 기반으로 GPT 전략 설계 프롬프트를 생성합니다.
    
    Args:
        claude_analysis (str): Claude의 분석 결과 텍스트
        input_data (Dict[str, Any]): 원본 입력 데이터
        
    Returns:
        str: GPT 전략 설계를 위한 프롬프트
    """
    try:
        # Claude 분석 결과에서 주요 섹션 추출
        sections = {
            "emotion_flow": "",
            "high_level_needs": [],
            "low_level_needs": [],
            "strategic_implications": ""
        }
        
        current_section = None
        for line in claude_analysis.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('[예상 감정 흐름]'):
                current_section = 'emotion_flow'
            elif line.startswith('[상위 욕구]'):
                current_section = 'high_level_needs'
            elif line.startswith('[하위 욕구]'):
                current_section = 'low_level_needs'
            elif line.startswith('[전략적 시사점 요약]'):
                current_section = 'strategic_implications'
            elif current_section:
                if current_section in ['high_level_needs', 'low_level_needs']:
                    if line and line[0].isdigit():
                        sections[current_section].append(line)
                else:
                    sections[current_section] += line + '\n'
        
        # GPT 전략 설계 프롬프트 생성
        prompt = f"""당신은 브랜드 전략 설계 전문가입니다.

[분석 결과]
{json.dumps(sections, ensure_ascii=False, indent=2)}

[브랜드 정보]
아이템명: {input_data.get("item_name")}
서비스 정의: {input_data.get("service_definition")}
핵심 타겟: {input_data.get("target_audience")}
사용 상황 시나리오: {input_data.get("usage_scenario")}
목표 포지셔닝: {input_data.get("desired_positioning")}

위 분석 결과를 바탕으로 다음 구조로 전략을 설계해주세요:

1. 브랜드 핵심 가치 제안
   - 감정 흐름에 기반한 핵심 가치
   - 상위/하위 욕구를 반영한 차별화 포인트

2. 포지셔닝 전략
   - 목표 시장 내 차별화 포지션
   - 경쟁사 대비 우위 요소

3. 커뮤니케이션 전략
   - 감정 흐름에 따른 메시지 전개
   - 욕구 충족을 위한 핵심 메시지

4. 실행 전략
   - 단계별 실행 계획
   - KPI 및 측정 지표

각 섹션은 구체적이고 실행 가능한 수준으로 작성해주세요.
"""
        return prompt
        
    except Exception as e:
        raise Exception(f"GPT 전략 설계 프롬프트 생성 중 오류 발생: {str(e)}") 