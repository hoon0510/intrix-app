"use client";

import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import StrategyResult from "@/components/analysis/StrategyResult";

export default function AnalysisPage() {
  const [tab, setTab] = useState('new');
  const router = useRouter();

  // 임시 데이터 - 실제로는 API에서 받아올 데이터
  const strategyData = {
    new: {
      title: "신규 유입 전략 요약",
      summary: "갤럭시 S25 울트라는 '기술적 우월성'과 '감성적 안정성'을 모두 충족시키는 프리미엄 디바이스입니다. 최첨단 기술과 사용자 경험의 완벽한 조화를 통해 시장에서 차별화된 위치를 확보할 수 있습니다.",
      slogans: [
        "바뀐 건 많지만, 바꾸지 않은 건 신뢰.",
        "기술이 앞서면, 감정도 따라옵니다.",
        "진화는 조용히, 신뢰는 강하게."
      ]
    },
    retention: {
      title: "리텐션 전략 요약",
      summary: "기존 사용자의 충성도를 높이기 위한 맞춤형 전략을 제안합니다. 개인화된 경험과 지속적인 가치 제공을 통해 장기적인 고객 관계를 구축할 수 있습니다.",
      slogans: [
        "당신만을 위한 맞춤 경험",
        "함께 성장하는 파트너십",
        "변화하는 당신을 위한 진화"
      ]
    },
    multi: {
      title: "다층 욕구 전략 요약",
      summary: "고객의 다양한 욕구 레이어를 분석하여 종합적인 전략을 제안합니다. 기능적, 감성적, 사회적 욕구를 모두 충족시키는 통합 솔루션을 제공합니다.",
      slogans: [
        "모든 욕구를 만족시키는 완벽한 선택",
        "기능과 감성을 넘어서는 경험",
        "당신의 모든 순간을 위한 솔루션"
      ]
    },
    report: {
      title: "리포트형 전략 요약",
      summary: "자세한 분석 결과와 실행 가능한 전략을 리포트 형태로 제공합니다. 데이터 기반의 인사이트와 구체적인 실행 방안을 통해 효과적인 마케팅 전략을 수립할 수 있습니다.",
      slogans: [
        "데이터로 보는 명확한 방향",
        "실행 가능한 구체적인 전략",
        "성공을 위한 단계별 가이드"
      ]
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-8 px-4">
        {/* 헤더 */}
        <div className="flex justify-between items-center mb-8">
          <Button
            variant="ghost"
            onClick={() => router.back()}
            className="flex items-center gap-2"
          >
            <ArrowLeft className="w-4 h-4" />
            이전으로
          </Button>
        </div>

        {/* 탭 네비게이션 */}
        <div className="bg-white rounded-xl shadow p-6">
          <Tabs value={tab} onValueChange={setTab} className="w-full">
            <TabsList className="grid w-full grid-cols-4 mb-6">
              <TabsTrigger 
                value="new"
                className="data-[state=active]:bg-blue-50 data-[state=active]:text-blue-600"
              >
                신규 유입 분석
              </TabsTrigger>
              <TabsTrigger 
                value="retention"
                className="data-[state=active]:bg-blue-50 data-[state=active]:text-blue-600"
              >
                리텐션 분석
              </TabsTrigger>
              <TabsTrigger 
                value="multi"
                className="data-[state=active]:bg-blue-50 data-[state=active]:text-blue-600"
              >
                다층 욕구 분석
              </TabsTrigger>
              <TabsTrigger 
                value="report"
                className="data-[state=active]:bg-blue-50 data-[state=active]:text-blue-600"
              >
                리포트형 분석
              </TabsTrigger>
            </TabsList>

            <TabsContent value="new" className="mt-4">
              <StrategyResult {...strategyData.new} />
            </TabsContent>

            <TabsContent value="retention" className="mt-4">
              <StrategyResult {...strategyData.retention} />
            </TabsContent>

            <TabsContent value="multi" className="mt-4">
              <StrategyResult {...strategyData.multi} />
            </TabsContent>

            <TabsContent value="report" className="mt-4">
              <StrategyResult {...strategyData.report} />
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
} 