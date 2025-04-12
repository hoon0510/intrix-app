# 📁 api/services/claude_service.py

import os
import httpx

# Claude API 키 및 엔드포인트
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

# 프롬프트 로딩 함수
def load_prompt():
    with open("prompts/prompt_claude_analysis.txt", "r", encoding="utf-8") as f:
        return f.read()

# 감정 및 욕구 분석 함수
async def analyze_emotion(input_text: str) -> dict:
    prompt = load_prompt().replace("{{input}}", input_text)

    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 1024,
        "temperature": 0.3,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(CLAUDE_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Claude 분석 실패: {response.text}")

    result_text = response.json()["content"][0]["text"]

    # GPT로 넘기기 위한 구조화된 결과 (여기선 텍스트 그대로 넘김)
    return {"raw": result_text, "source": "claude"}
