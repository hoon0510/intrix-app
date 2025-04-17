"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Layout from "@/components/layout";

export default function AnalyzeProcessingPage() {
  const router = useRouter();

  useEffect(() => {
    const timer = setTimeout(() => {
      // 예시로 3초 후에 결과 페이지로 리디렉션
      router.push("/analyze/result?result=📌 분석 결과 예시 텍스트입니다. (실제 데이터 연동 예정)");
    }, 3000);

    return () => clearTimeout(timer);
  }, [router]);

  return (
    <Layout>
      <div className="flex flex-col items-center justify-center h-screen bg-gray-50 px-4">
        <h1 className="text-3xl font-semibold mb-6 text-center">🔍 분석을 진행 중입니다</h1>
        <p className="text-gray-600 text-center mb-4">
          감정, 욕구, 전략을 분석하는 중입니다. 잠시만 기다려 주세요...
        </p>
        <div className="w-48 h-1.5 bg-gray-200 rounded-full overflow-hidden">
          <div className="h-full bg-blue-500 animate-pulse w-2/3"></div>
        </div>
      </div>
    </Layout>
  );
} 