"use client";

import { useSearchParams } from "next/navigation";
import Layout from "@/components/layout";

export default function AnalyzeResultPage() {
  const searchParams = useSearchParams();
  const result = searchParams.get("result") || "분석 결과를 불러오는 중입니다...";

  return (
    <Layout>
      <div className="max-w-3xl mx-auto py-20 px-6">
        <h1 className="text-3xl font-bold mb-6">📊 분석 결과</h1>
        <div className="bg-gray-50 border p-6 rounded-lg shadow-sm text-sm whitespace-pre-wrap">
          {result}
        </div>
      </div>
    </Layout>
  );
} 