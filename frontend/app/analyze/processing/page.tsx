"use client";

import { useEffect } from "react";
import Layout from "@/components/layout/Layout";

export default function AnalyzeProcessingPage() {
  useEffect(() => {
    // 분석 요청 및 결과 페이지로 리다이렉트
  }, []);

  return (
    <Layout>
      <div className="max-w-2xl mx-auto py-20 px-6 text-center">
        <h1 className="text-3xl font-bold mb-6">분석 중입니다...</h1>
        <p className="text-gray-600">잠시만 기다려주세요.</p>
      </div>
    </Layout>
  );
} 