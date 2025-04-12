# 📁 api/services/gpt_service.py

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# 프롬프트 불러오기 함수

def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# 전략 설계 함수
async def generate_strategy(analysis_result: dict) -> dict:
    prompt_template = load_prompt("prompts/prompt_gpt_strategy.txt")
    prompt = prompt_template.replace("{{analysis}}", analysis_result["raw"])

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        temperature=0.4,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# 카피라이팅 생성 함수
async def generate_copy(analysis_result: dict) -> dict:
    prompt_template = load_prompt("prompts/prompt_gpt_copywriting.txt")
    prompt = prompt_template.replace("{{analysis}}", analysis_result["raw"])

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        temperature=0.8,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# 퍼포먼스 전략 설계 함수
async def generate_performance(analysis_result: dict) -> dict:
    prompt_template = load_prompt("prompts/prompt_gpt_performance.txt")
    prompt = prompt_template.replace("{{analysis}}", analysis_result["raw"])

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        temperature=0.5,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]
