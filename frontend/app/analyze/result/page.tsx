"use client";

import Layout from "@/components/layout";
import StrategySlogan from "@/components/StrategySlogan";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

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

  // TODO: PDF 다운로드 기능 연동 (Claude 포맷 결과 기반)
  const handleDownload = () => {
    console.log("Download PDF");
  };

  // TODO: 공유 링크 생성 기능 연동 (history_id 기반 URL)
  const handleShare = () => {
    console.log("Copy share link");
  };

  return (
    <Layout>
      <div className="max-w-3xl mx-auto mt-20 px-6">
        <h1 className="text-3xl font-bold mb-8 text-center">📊 분석 결과 요약</h1>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4">{dummyStrategy.title}</h2>
          <p className="mb-6 text-gray-700 leading-relaxed">{dummyStrategy.summary}</p>
          <StrategySlogan slogans={dummyStrategy.slogans} />
          
          <Card className="bg-gray-50 border border-gray-200 shadow-sm mt-6">
            <CardHeader>
              <CardTitle>감정 흐름 요약</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm text-gray-700">
              <p><strong>1차 감정:</strong> 기대 → 안정</p>
              <p><strong>주요 욕구:</strong> 신뢰, 기능성, 장기적 가치</p>
              <p><strong>전환 메커니즘:</strong> 기술 → 감정 안정 → 일관성</p>
            </CardContent>
          </Card>

          <Card className="bg-white border border-gray-200 shadow-md mt-6">
            <CardHeader>
              <CardTitle>브랜딩 확장 전략</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-gray-700 space-y-2">
              <p><strong>기존 인식 (Reference Point):</strong> 기술적 혁신 = 복잡함</p>
              <p><strong>프레임 전환 전략:</strong> '혁신'보다 '신뢰'를 중심 가치로 재정의</p>
              <p><strong>포지셔닝 문장:</strong> "진화는 조용히, 신뢰는 강하게."</p>
            </CardContent>
          </Card>
          
          <div className="flex space-x-4 mt-6">
            <button 
              onClick={handleDownload}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              전략 PDF 다운로드
            </button>
            <button 
              onClick={handleShare}
              className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              공유 링크 복사
            </button>
          </div>

          <div className="text-xs text-center text-gray-500 mt-10 mb-4 px-4">
            <hr className="my-4 border-gray-300" />
            <p>
              전략 자동화 책임 안내<br />
              Intrix는 고객의 감정과 욕구 분석을 기반으로 전략과 카피를 자동 생성합니다. 저희 시스템은 데이터 기반 인사이트를 제공하지만, 그 결과에 대한 가치 판단은 하지 않습니다. 제안된 전략의 윤리적 적합성과 실행 여부는 전적으로 이용자의 판단에 달려 있습니다. Intrix는 전략 자동화를 위한 도구로서, 최종 결정과 그에 따른 윤리적 책임은 사용자에게 있음을 안내드립니다.
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
} 