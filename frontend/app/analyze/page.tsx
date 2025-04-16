"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import Layout from "@/components/layout";

export default function AnalyzePage() {
  const router = useRouter();
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() === "") return;
    router.push("/analyze/processing"); // 분석 중 페이지로 이동
  };

  return (
    <Layout>
      <div className="max-w-xl mx-auto mt-24">
        <h1 className="text-3xl font-bold mb-6 text-center">리뷰 기반 감정·욕구 분석</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none"
            placeholder="예: 갤럭시 S25 울트라"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button
            type="submit"
            className="w-full py-3 bg-black text-white rounded-md font-semibold hover:bg-gray-800"
          >
            분석 요청하기
          </button>
        </form>
      </div>
    </Layout>
  );
} 