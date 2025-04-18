import os
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    async def analyze_with_gpt(self, text: str, analysis_type: str) -> dict:
        # 분석 유형에 따른 프롬프트 설정
        prompts = {
            "new": "다음 텍스트에 대해 신규 유입 관점에서 분석해주세요. 주요 포인트와 추천 사항을 포함해주세요:",
            "retention": "다음 텍스트에 대해 리텐션 관점에서 분석해주세요. 패턴과 제안 사항을 포함해주세요:",
            "desire": "다음 텍스트에 대해 다층 욕구 구조를 분석해주세요. 욕구 계층과 인사이트를 포함해주세요:",
            "report": "다음 텍스트에 대해 전략 보고서 형식으로 분석해주세요. 요약과 전략을 포함해주세요:"
        }

        prompt = prompts.get(analysis_type, prompts["new"])
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "당신은 전문적인 브랜드 전략 분석가입니다."},
                    {"role": "user", "content": f"{prompt}\n\n{text}"}
                ]
            )
            return self._parse_gpt_response(response.choices[0].message.content)
        except Exception as e:
            print(f"GPT Error: {e}")
            return await self.analyze_with_claude(text, analysis_type)

    async def analyze_with_claude(self, text: str, analysis_type: str) -> dict:
        prompts = {
            "new": "신규 유입 분석\n- 주요 포인트\n- 추천 사항",
            "retention": "리텐션 분석\n- 패턴\n- 제안 사항",
            "desire": "다층 욕구 분석\n- 욕구 계층\n- 인사이트",
            "report": "전략 보고서\n- 요약\n- 전략"
        }

        prompt = prompts.get(analysis_type, prompts["new"])
        
        try:
            response = await self.anthropic_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": f"다음 텍스트를 분석해주세요. 결과는 다음 형식으로 작성해주세요:\n\n{prompt}\n\n분석할 텍스트:\n{text}"
                    }
                ]
            )
            return self._parse_claude_response(response.content)
        except Exception as e:
            print(f"Claude Error: {e}")
            return self._get_fallback_response(analysis_type)

    def _parse_gpt_response(self, response: str) -> dict:
        # GPT 응답을 구조화된 형식으로 변환
        try:
            lines = response.split("\n")
            result = {}
            current_key = None
            current_items = []

            for line in lines:
                if line.strip().endswith(":"):
                    if current_key and current_items:
                        result[current_key] = current_items
                    current_key = line.strip(":")
                    current_items = []
                elif line.strip().startswith("- "):
                    current_items.append(line.strip("- "))
                elif line.strip():
                    if not current_key:
                        current_key = "summary"
                    current_items.append(line.strip())

            if current_key and current_items:
                result[current_key] = current_items

            return result
        except:
            return self._get_fallback_response("new")

    def _parse_claude_response(self, response: str) -> dict:
        # Claude 응답을 구조화된 형식으로 변환
        try:
            return self._parse_gpt_response(response)  # 동일한 파싱 로직 사용
        except:
            return self._get_fallback_response("new")

    def _get_fallback_response(self, analysis_type: str) -> dict:
        # AI 서비스 실패 시 기본 응답
        fallback_responses = {
            "new": {
                "key_points": ["초기 반응 분석 필요", "데이터 수집 중"],
                "recommendations": ["추가 데이터 수집 권장", "상세 분석 준비"]
            },
            "retention": {
                "patterns": ["패턴 분석 진행 중", "데이터 확인 필요"],
                "suggestions": ["데이터 보강 필요", "추가 모니터링 권장"]
            },
            "desire": {
                "layers": ["기본적 욕구", "심층 분석 필요"],
                "insights": ["추가 데이터 필요", "상세 분석 대기"]
            },
            "report": {
                "summary": "분석 준비 중",
                "strategies": ["데이터 수집", "전략 수립 예정"]
            }
        }
        return fallback_responses.get(analysis_type, fallback_responses["new"])

ai_service = AIService() 