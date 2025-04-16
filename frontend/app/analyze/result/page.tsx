"use client";

import Layout from "@/components/layout";
import StrategySlogan from "@/components/StrategySlogan";

export default function AnalyzeResultPage() {
  const dummyStrategy = {
    title: "전략 요약",
    summary:
      "갤럭시 S25 울트라는 '기술적 우월성'과 '감성적 안정성'을 모두 충족시키는 프리미엄 디바이스입니다. 감정 분석 결과, 사용자들은 혁신적 기능보다는 신뢰성과 일관성에서 더 높은 가치를 느끼고 있으며, 이를 기반으로 '일관된 진화'라는 전략 방향이 도출되었습니다.",
    slogans: [
      "바뀐 건 많지만, 바꾸지 않은 건 신뢰.",
      "기술이 앞서면, 감정도 따라옵니다.",
      "진화는 조용히, 신뢰는 강하게.",
    ],
  };

  return (
    <Layout>
      <div className="max-w-3xl mx-auto mt-20 px-6">
        <h1 className="text-3xl font-bold mb-8 text-center">📊 분석 결과 요약</h1>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4">{dummyStrategy.title}</h2>
          <p className="mb-6 text-gray-700 leading-relaxed">{dummyStrategy.summary}</p>
          <StrategySlogan slogans={dummyStrategy.slogans} />
        </div>
      </div>
    </Layout>
  );
} 