"use client";

import React from "react";
import { useState, useEffect } from "react";
import { toast } from "react-toastify";

export default function DeveloperClient() {
  const [apiKey, setApiKey] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchApiKey();
  }, []);

  const fetchApiKey = async () => {
    try {
      const response = await fetch("/api/api-key");
      if (response.ok) {
        const data = await response.json();
        setApiKey(data.api_key);
      }
    } catch (error) {
      console.error("API 키 조회 중 오류 발생:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const generateApiKey = async () => {
    try {
      const response = await fetch("/api/api-access/register", {
        method: "POST",
      });
      
      if (response.ok) {
        const data = await response.json();
        setApiKey(data.api_key);
        toast.success("API 키가 발급되었습니다");
      } else {
        throw new Error("API 키 발급 실패");
      }
    } catch (error) {
      console.error("API 키 발급 중 오류 발생:", error);
      toast.error("API 키 발급에 실패했습니다");
    }
  };

  const copyToClipboard = () => {
    if (apiKey) {
      navigator.clipboard.writeText(apiKey);
      toast.success("API 키가 복사되었습니다");
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <h1 className="text-3xl font-bold mb-8">개발자 포털</h1>
      
      {/* API Key Section */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">API 키 관리</h2>
        {isLoading ? (
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-3/4"></div>
          </div>
        ) : apiKey ? (
          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <input
                type="text"
                value={apiKey}
                readOnly
                className="flex-1 p-2 border rounded bg-gray-50 font-mono text-sm"
              />
              <button
                onClick={copyToClipboard}
                className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
              >
                복사
              </button>
            </div>
          </div>
        ) : (
          <button
            onClick={generateApiKey}
            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
          >
            API 키 발급
          </button>
        )}
      </div>

      {/* Documentation Section */}
      <div className="space-y-8">
        <section>
          <h2 className="text-xl font-semibold mb-4">API 키 설명</h2>
          <p className="text-gray-600 mb-4">
            API 키는 Intrix API를 사용하기 위한 인증 수단입니다. 각 사용자에게 발급되는 고유한 키를 통해 API를 호출할 수 있습니다.
          </p>
        </section>

        <section>
          <h2 className="text-xl font-semibold mb-4">호출 제한</h2>
          <ul className="list-disc pl-6 text-gray-600 space-y-2">
            <li>분당 최대 60회 호출 가능</li>
            <li>일일 최대 10,000회 호출 가능</li>
            <li>동시 요청은 최대 10개까지 허용</li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-semibold mb-4">API 사용 가이드</h2>
          
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium mb-2">1. 필수 요청 헤더</h3>
              <div className="bg-gray-800 rounded-lg p-4">
                <pre className="text-gray-200 text-sm overflow-x-auto">
                  <code>
{`// 모든 API 요청에 필수로 포함되어야 하는 헤더
{
  "Content-Type": "application/json",
  "API-Key": "${apiKey || 'YOUR_API_KEY'}"
}`}
                  </code>
                </pre>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-medium mb-2">2. JavaScript/TypeScript 사용 예시</h3>
              <div className="bg-gray-800 rounded-lg p-4">
                <pre className="text-gray-200 text-sm overflow-x-auto">
                  <code>
{`// API 키 설정
const API_KEY = '${apiKey || 'YOUR_API_KEY'}';

// 전략 생성 API 호출
async function generateStrategy(inputText, channels) {
  const response = await fetch('https://api.intrix.com/api-access/strategy', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'API-Key': API_KEY
    },
    body: JSON.stringify({
      input_text: inputText,
      channels: channels
    })
  });

  if (!response.ok) {
    throw new Error('API 호출 실패');
  }

  return await response.json();
}

// 사용 예시
const result = await generateStrategy(
  '브랜드 분석 텍스트',
  ['community', 'sns']
);`}
                  </code>
                </pre>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-medium mb-2">3. Python 사용 예시</h3>
              <div className="bg-gray-800 rounded-lg p-4">
                <pre className="text-gray-200 text-sm overflow-x-auto">
                  <code>
{`import requests

# API 키 설정
API_KEY = '${apiKey || 'YOUR_API_KEY'}'

# 전략 생성 API 호출
def generate_strategy(input_text, channels):
    url = 'https://api.intrix.com/api-access/strategy'
    headers = {
        'Content-Type': 'application/json',
        'API-Key': API_KEY
    }
    data = {
        'input_text': input_text,
        'channels': channels
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

# 사용 예시
result = generate_strategy(
    '브랜드 분석 텍스트',
    ['community', 'sns']
)`}
                  </code>
                </pre>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-medium mb-2">4. 응답 예시</h3>
              <div className="bg-gray-800 rounded-lg p-4">
                <pre className="text-gray-200 text-sm overflow-x-auto">
                  <code>
{`{
  "copy": "브랜드 카피",
  "style": "감성적",
  "report_html": "<div>...</div>"
}`}
                  </code>
                </pre>
              </div>
              <div className="mt-4 space-y-2">
                <h4 className="font-medium">응답 필드 설명:</h4>
                <ul className="list-disc pl-6 text-gray-600 space-y-1">
                  <li><code className="bg-gray-100 px-1 rounded">copy</code>: 생성된 브랜드 카피</li>
                  <li><code className="bg-gray-100 px-1 rounded">style</code>: 브랜드 스타일 (감성적/이성적)</li>
                  <li><code className="bg-gray-100 px-1 rounded">report_html</code>: HTML 형식의 분석 리포트</li>
                </ul>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-medium mb-2">5. 에러 응답</h3>
              <div className="bg-gray-800 rounded-lg p-4">
                <pre className="text-gray-200 text-sm overflow-x-auto">
                  <code>
{`{
  "error": "에러 메시지"
}`}
                  </code>
                </pre>
              </div>
              <div className="mt-4 space-y-2">
                <h4 className="font-medium">에러 코드:</h4>
                <ul className="list-disc pl-6 text-gray-600 space-y-1">
                  <li><code className="bg-gray-100 px-1 rounded">400</code>: 잘못된 요청</li>
                  <li><code className="bg-gray-100 px-1 rounded">401</code>: 인증 실패</li>
                  <li><code className="bg-gray-100 px-1 rounded">403</code>: 권한 없음</li>
                  <li><code className="bg-gray-100 px-1 rounded">429</code>: 요청 제한 초과</li>
                  <li><code className="bg-gray-100 px-1 rounded">500</code>: 서버 오류</li>
                </ul>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
} 