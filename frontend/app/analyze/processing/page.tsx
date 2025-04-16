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
      <div className="flex flex-col items-center justify-center h-[80vh] space-y-6">
        <div className="text-2xl font-semibold">분석 중입니다...</div>
        <div className="animate-pulse text-sm text-gray-500">AI가 감정과 욕구를 분석하고 있어요</div>
      </div>
    </Layout>
  );
} 