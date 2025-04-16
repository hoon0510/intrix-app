import React, { useState } from "react";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "../components/ui/tabs";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";

const dummyResults = [
  {
    title: "신규유입 분석",
    description: "고객의 최초 접점에서 감정의 흐름과 전환 포인트 분석",
    details: "1차 감정: 기대감 → 정보 탐색 욕구 → CTA 클릭",
    date: "2024-04-22",
  },
  {
    title: "리텐션 분석",
    description: "기존 고객의 재방문/재사용을 유도한 핵심 감정 구조",
    details: "1차 감정: 익숙함 → 신뢰 → 반복사용 욕구",
    date: "2024-04-21",
  },
  {
    title: "다층 욕구 기반 분석",
    description: "상위/하위 욕구 분해를 통한 무의식 유도 전략 도출",
    details: "상위 욕구: 사회적 인정 / 하위 욕구: 정서적 안정",
    date: "2024-04-20",
  },
];

export default function IntrixUI() {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  const toggleExpand = (index: number) => {
    setExpandedIndex((prev) => (prev === index ? null : index));
  };

  return (
    <main className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">INTRIX 분석 결과</h1>
      <Tabs defaultValue="analysis" className="w-full">
        <TabsList className="mb-4">
          <TabsTrigger value="analysis">분석 결과</TabsTrigger>
          <TabsTrigger value="favorite">즐겨찾기</TabsTrigger>
          <TabsTrigger value="history">이력 관리</TabsTrigger>
        </TabsList>
        <TabsContent value="analysis">
          <div className="space-y-4">
            {dummyResults.map((result, index) => (
              <Card key={index} className="border border-gray-200">
                <CardHeader>
                  <CardTitle>{result.title}</CardTitle>
                  <CardDescription>{result.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-700">{result.date}</p>
                </CardContent>
                {expandedIndex === index && (
                  <CardContent>
                    <p>{result.details}</p>
                  </CardContent>
                )}
                <CardFooter className="flex justify-between">
                  <Button variant="outline" onClick={() => toggleExpand(index)}>
                    {expandedIndex === index ? "접기" : "자세히 보기"}
                  </Button>
                  <div className="space-x-2">
                    <Button variant="ghost">다운로드</Button>
                    <Badge variant="default">NEW</Badge>
                  </div>
                </CardFooter>
              </Card>
            ))}
          </div>
        </TabsContent>
        <TabsContent value="favorite">
          <p>즐겨찾기 탭 (구현 예정)</p>
        </TabsContent>
        <TabsContent value="history">
          <p>이력 관리 탭 (구현 예정)</p>
        </TabsContent>
      </Tabs>
    </main>
  );
}
