"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { UserIcon, PlusIcon } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import DownloadSection from "@/components/DownloadSection";
import ResultRenderer from "@/components/ResultRenderer";
import Navbar from "@/components/Navbar";

// 임시 데이터 - 실제로는 API에서 받아올 데이터
const dummyResult = {
  title: "전략 요약",
  summary: "갤럭시 S25 울트라는 신뢰와 진화를 핵심으로 한 전략입니다. 기술적 우월성과 감성적 안정성을 모두 충족시키는 프리미엄 디바이스로서, 사용자들의 신뢰를 바탕으로 지속적인 진화를 추구합니다.",
  slogans: [
    "신뢰는 그대로, 진화는 조용히.",
    "바뀐 건 많지만, 바꾸지 않은 건 중심."
  ],
  upperDesires: [
    "심리적 안정",
    "목표 달성",
    "개성 표현"
  ],
  lowerDesires: [
    "정서적 안정",
    "실패 회피",
    "자기애 강화"
  ],
  emotionFlow: [
    "신뢰",
    "냉소",
    "설득",
    "호감",
    "전환"
  ],
  executionStrategy: {
    hook: "당신의 신뢰를 바탕으로 한 진화",
    flow: "신뢰 형성 → 가치 제안 → 감정 전환",
    cta: "지금 바로 새로운 경험을 시작하세요"
  }
};

export default function ResultPage() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="container mx-auto px-4 py-8">
        {/* Strategy Summary Section */}
        <section className="mb-6">
          <h2 className="text-2xl font-semibold">📊 전략 요약</h2>
          <p className="text-gray-700 mt-2">
            아래는 Intrix가 분석한 전략 결과 요약입니다. 분석 항목별로 구체적인 전략 설계와 전환 흐름을 시각적으로 확인할 수 있습니다.
          </p>
        </section>

        {/* Strategy Visualization Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 mb-8">
          <div className="border p-4 rounded-xl shadow-sm bg-white">
            <h3 className="text-lg font-bold mb-2">전략 방향</h3>
            <p className="text-gray-800">일관된 진화, 감정적 안정성 기반 포지셔닝</p>
          </div>
          <div className="border p-4 rounded-xl shadow-sm bg-white">
            <h3 className="text-lg font-bold mb-2">프레임 전환 전략</h3>
            <p className="text-gray-800">기술 중심 → 감정 중심의 신뢰 강조</p>
          </div>
          <div className="border p-4 rounded-xl shadow-sm bg-white">
            <h3 className="text-lg font-bold mb-2">대표 슬로건</h3>
            <p className="text-gray-800">"바뀐 건 많지만, 바꾸지 않은 건 신뢰."</p>
          </div>
        </div>

        {/* Existing Analysis Results Section */}
        <div className="max-w-4xl mx-auto space-y-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold mb-4">분석 결과</h1>
            <p className="text-gray-600">AI가 분석한 전략과 브랜딩 결과입니다.</p>
          </div>

          {/* 전략 요약 */}
          <Card>
            <CardHeader>
              <CardTitle>{dummyResult.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">{dummyResult.summary}</p>
              <div className="flex flex-wrap gap-2 mt-4">
                {dummyResult.slogans.map((slogan, index) => (
                  <Badge key={index} variant="outline">
                    {slogan}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>

          <Separator />

          {/* 욕구 분석 */}
          <div className="grid md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>상위 욕구</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {dummyResult.upperDesires.map((desire, index) => (
                    <li key={index} className="flex items-center gap-2">
                      <span className="text-primary">•</span>
                      <span className="text-muted-foreground">{desire}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>하위 욕구</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {dummyResult.lowerDesires.map((desire, index) => (
                    <li key={index} className="flex items-center gap-2">
                      <span className="text-primary">•</span>
                      <span className="text-muted-foreground">{desire}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </div>

          <Separator />

          {/* 감정 흐름 */}
          <Card>
            <CardHeader>
              <CardTitle>감정 흐름</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                {dummyResult.emotionFlow.map((emotion, index) => (
                  <div key={index} className="flex flex-col items-center">
                    <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-2">
                      <span className="text-primary font-semibold">{emotion}</span>
                    </div>
                    {index < dummyResult.emotionFlow.length - 1 && (
                      <div className="w-16 h-1 bg-primary/20" />
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Separator />

          {/* 실행 전략 */}
          <Card>
            <CardHeader>
              <CardTitle>실행 전략</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h3 className="font-semibold mb-2">Hook</h3>
                <p className="text-muted-foreground">{dummyResult.executionStrategy.hook}</p>
              </div>
              <div>
                <h3 className="font-semibold mb-2">Flow</h3>
                <p className="text-muted-foreground">{dummyResult.executionStrategy.flow}</p>
              </div>
              <div>
                <h3 className="font-semibold mb-2">CTA</h3>
                <p className="text-muted-foreground">{dummyResult.executionStrategy.cta}</p>
              </div>
            </CardContent>
          </Card>

          {/* 다운로드 섹션 */}
          <DownloadSection downloadUrl="/api/download-report" />

          {/* CTA 버튼 */}
          <div className="flex flex-col sm:flex-row gap-4">
            <Button
              variant="outline"
              onClick={() => router.push("/mypage")}
              className="flex items-center gap-2"
            >
              <UserIcon className="w-4 h-4" />
              마이페이지로 이동
            </Button>
            <Button
              onClick={() => router.push("/analyze")}
              className="flex items-center gap-2"
            >
              <PlusIcon className="w-4 h-4" />
              새로운 분석 시작
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
} 