"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface StrategyData {
  title: string;
  summary: string;
  desireFlow?: string[];
  positioning: string;
  slogans: string[];
  brandingStrategies: string[];
  executionStrategy: {
    hook: string;
    flow: string;
    cta: string;
  };
}

interface ResultRendererProps {
  data: StrategyData;
}

export default function ResultRenderer({ data }: ResultRendererProps) {
  return (
    <div className="space-y-8">
      {/* 전략 제목 및 요약 */}
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">{data.title}</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">{data.summary}</p>
        </CardContent>
      </Card>

      {/* 주요 욕구 흐름 */}
      {data.desireFlow && data.desireFlow.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>주요 욕구 흐름</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="list-disc list-inside space-y-2">
              {data.desireFlow.map((flow, index) => (
                <li key={index} className="text-muted-foreground">
                  {flow}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {/* 포지셔닝 */}
      <Card>
        <CardHeader>
          <CardTitle>브랜드 포지셔닝</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">{data.positioning}</p>
        </CardContent>
      </Card>

      {/* 슬로건 */}
      <Card>
        <CardHeader>
          <CardTitle>슬로건</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {data.slogans.map((slogan, index) => (
              <Badge key={index} variant="outline">
                {slogan}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* 브랜딩 전략 */}
      <Card>
        <CardHeader>
          <CardTitle>브랜딩 전략</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="list-disc list-inside space-y-2">
            {data.brandingStrategies.map((strategy, index) => (
              <li key={index} className="text-muted-foreground">
                {strategy}
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>

      {/* 실행 전략 */}
      <Card>
        <CardHeader>
          <CardTitle>실행 전략</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h3 className="font-semibold mb-2">Hook</h3>
            <p className="text-muted-foreground">{data.executionStrategy.hook}</p>
          </div>
          <div>
            <h3 className="font-semibold mb-2">Flow</h3>
            <p className="text-muted-foreground">{data.executionStrategy.flow}</p>
          </div>
          <div>
            <h3 className="font-semibold mb-2">CTA</h3>
            <p className="text-muted-foreground">{data.executionStrategy.cta}</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
} 