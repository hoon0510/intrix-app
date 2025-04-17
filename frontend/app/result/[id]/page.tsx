"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

interface AnalysisResult {
  job_id: string;
  status: "processing" | "completed" | "failed";
  result?: {
    keyword: string;
    channels: string[];
    analysis: {
      emotions: string[];
      desires: string[];
      strategy: string;
      branding: string;
      copywriting: string;
    };
  };
}

export default function ResultPage() {
  const params = useParams();
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResult = async () => {
      try {
        const res = await fetch(`/api/analysis/${params.id}`);
        const data = await res.json();
        setResult(data);
      } catch (error) {
        console.error("결과 조회 중 오류 발생:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchResult();
  }, [params.id]);

  if (loading) {
    return (
      <section className="w-full max-w-5xl mx-auto py-10">
        <h1 className="text-3xl font-semibold mb-4">분석 결과</h1>
        <p>결과를 불러오는 중입니다...</p>
      </section>
    );
  }

  if (!result) {
    return (
      <section className="w-full max-w-5xl mx-auto py-10">
        <h1 className="text-3xl font-semibold mb-4">분석 결과</h1>
        <p>결과를 불러오는데 실패했습니다.</p>
      </section>
    );
  }

  if (result.status === "processing") {
    return (
      <section className="w-full max-w-5xl mx-auto py-10">
        <h1 className="text-3xl font-semibold mb-4">분석 결과</h1>
        <p>분석이 진행 중입니다. 잠시만 기다려주세요...</p>
      </section>
    );
  }

  if (result.status === "failed") {
    return (
      <section className="w-full max-w-5xl mx-auto py-10">
        <h1 className="text-3xl font-semibold mb-4">분석 결과</h1>
        <p>분석 중 오류가 발생했습니다.</p>
      </section>
    );
  }

  return (
    <section className="w-full max-w-5xl mx-auto py-10">
      <h1 className="text-3xl font-semibold mb-4">분석 결과</h1>
      <div className="space-y-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2">키워드</h2>
          <p>{result.result?.keyword}</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2">선택된 채널</h2>
          <ul className="list-disc list-inside">
            {result.result?.channels.map((channel) => (
              <li key={channel}>{channel}</li>
            ))}
          </ul>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2">감정 분석</h2>
          <ul className="list-disc list-inside">
            {result.result?.analysis.emotions.map((emotion) => (
              <li key={emotion}>{emotion}</li>
            ))}
          </ul>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2">욕구 분석</h2>
          <ul className="list-disc list-inside">
            {result.result?.analysis.desires.map((desire) => (
              <li key={desire}>{desire}</li>
            ))}
          </ul>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2">전략 제안</h2>
          <p>{result.result?.analysis.strategy}</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2">브랜딩 방향</h2>
          <p>{result.result?.analysis.branding}</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2">카피라이팅</h2>
          <p>{result.result?.analysis.copywriting}</p>
        </div>
      </div>
    </section>
  );
} 