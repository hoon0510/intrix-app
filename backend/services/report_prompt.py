from typing import Dict, Any
import json

def generate_report_prompt(
    claude_analysis: str,
    gpt_strategy: str,
    input_data: Dict[str, Any]
) -> str:
    """
    분석 결과와 전략을 기반으로 리포트 생성을 위한 프롬프트를 생성합니다.
    
    Args:
        claude_analysis (str): Claude의 감정/욕구 분석 결과
        gpt_strategy (str): GPT의 전략 설계 결과
        input_data (Dict[str, Any]): 원본 입력 데이터
        
    Returns:
        str: 리포트 생성을 위한 프롬프트
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
        
        # GPT 전략 결과에서 주요 섹션 추출
        strategy_sections = {
            "brand_value": "",
            "positioning": "",
            "communication": "",
            "execution": ""
        }
        
        current_section = None
        for line in gpt_strategy.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('1. 브랜드 핵심 가치 제안'):
                current_section = 'brand_value'
            elif line.startswith('2. 포지셔닝 전략'):
                current_section = 'positioning'
            elif line.startswith('3. 커뮤니케이션 전략'):
                current_section = 'communication'
            elif line.startswith('4. 실행 전략'):
                current_section = 'execution'
            elif current_section:
                strategy_sections[current_section] += line + '\n'
        
        # 리포트 생성을 위한 프롬프트 생성
        prompt = f"""당신은 전문 마케팅 리포트 작성 AI입니다.

[브랜드 정보]
아이템명: {input_data.get("item_name")}
서비스 정의: {input_data.get("service_definition")}
핵심 타겟: {input_data.get("target_audience")}
사용 상황 시나리오: {input_data.get("usage_scenario")}
목표 포지셔닝: {input_data.get("desired_positioning")}

[감정/욕구 분석 결과]
{json.dumps(sections, ensure_ascii=False, indent=2)}

[전략 설계 결과]
{json.dumps(strategy_sections, ensure_ascii=False, indent=2)}

위 정보를 바탕으로 다음 구조로 전문적인 마케팅 리포트를 작성해주세요:

1. 실행 요약 (Executive Summary)
   - 핵심 분석 결과 요약
   - 주요 전략 방향성
   - 기대 효과

2. 감정/욕구 분석 상세
   - 감정 흐름 분석
   - 상위/하위 욕구 구조
   - 전략적 시사점

3. 브랜드 전략
   - 핵심 가치 제안
   - 포지셔닝 전략
   - 커뮤니케이션 전략

4. 실행 계획
   - 단계별 실행 로드맵
   - KPI 및 측정 지표
   - 리스크 관리 방안

5. 부록
   - 참고 자료
   - 용어 설명
   - 추가 분석 데이터

각 섹션은 전문적이고 체계적인 구조로 작성하며, 
실무자가 바로 활용할 수 있는 수준의 구체적인 내용을 포함해주세요.
"""
        return prompt
        
    except Exception as e:
        raise Exception(f"리포트 생성 프롬프트 생성 중 오류 발생: {str(e)}") 