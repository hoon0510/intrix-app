"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function AnalyzePage() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleAnalyze = async () => {
    if (!input.trim()) return;
    
    try {
      setLoading(true);
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input }),
      });
      
      if (!res.ok) {
        throw new Error("분석 요청에 실패했습니다.");
      }
      
      const data = await res.json();
      setResult(data);
      router.push("/mypage");
    } catch (error) {
      console.error("Error:", error);
      alert("분석 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-4">
      <div className="space-y-2">
        <label htmlFor="input" className="block text-sm font-medium text-gray-700">
          리뷰나 문장을 입력하세요
        </label>
        <textarea
          id="input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="분석할 텍스트를 입력하세요..."
          className="w-full border p-3 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          rows={4}
          disabled={loading}
        />
      </div>
      
      <button
        onClick={handleAnalyze}
        disabled={loading || !input.trim()}
        className="w-full px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {loading ? "분석 중..." : "분석하기"}
      </button>

      {result && (
        <div className="mt-4 p-4 border rounded-xl bg-gray-50 space-y-4">
          <div className="space-y-2">
            <h3 className="font-medium text-gray-900">감정 분석 결과</h3>
            <pre className="text-sm text-gray-600 whitespace-pre-wrap">
              {JSON.stringify(result.emotion_analysis, null, 2)}
            </pre>
          </div>
          
          <div className="space-y-2">
            <h3 className="font-medium text-gray-900">전략 제안</h3>
            <pre className="text-sm text-gray-600 whitespace-pre-wrap">
              {JSON.stringify(result.strategy, null, 2)}
            </pre>
          </div>
          
          <div className="space-y-2">
            <h3 className="font-medium text-gray-900">카피라이팅</h3>
            <pre className="text-sm text-gray-600 whitespace-pre-wrap">
              {JSON.stringify(result.copywriting, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
} 