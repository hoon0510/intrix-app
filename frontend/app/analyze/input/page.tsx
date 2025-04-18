"use client";

import { useState } from "react";
import Layout from "@/components/layout/Layout";

export default function AnalyzeInputPage() {
  const [inputText, setInputText] = useState("");
  const [useSample, setUseSample] = useState(false);

  const handleSampleClick = () => {
    setInputText("처음엔 기대도 안했는데, 쓰다보니 진짜 괜찮더라고요. 딱 필요한 기능만 있어서 더 편했어요.");
    setUseSample(true);
  };

  const handleSubmit = () => {
    if (!inputText.trim()) return alert("리뷰 데이터를 입력해주세요.");
    // 분석 페이지 이동 (예: /analyze/result?data=...)
  };

  return (
    <Layout>
      <div className="max-w-2xl mx-auto py-20 px-6">
        <h1 className="text-3xl font-bold mb-6">리뷰 데이터를 입력해주세요</h1>
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="예: 이 앱 덕분에 스트레스가 줄었어요. 매일 사용 중입니다."
          className="w-full h-40 p-4 border border-gray-300 rounded-lg resize-none text-sm"
        />
        <div className="flex items-center justify-between mt-4">
          <button
            onClick={handleSampleClick}
            className="text-sm underline text-gray-600 hover:text-black"
          >
            샘플 리뷰 불러오기
          </button>
          <button
            onClick={handleSubmit}
            className="bg-black text-white px-6 py-2 rounded hover:bg-gray-800"
          >
            분석 요청 →
          </button>
        </div>
        {useSample && (
          <p className="text-xs text-gray-400 mt-2">
            * 샘플 데이터가 자동 입력되었습니다.
          </p>
        )}
      </div>
    </Layout>
  );
} 