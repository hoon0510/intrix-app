"use client";

import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function StrategyPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-start px-4 py-8 bg-white">
      <section className="w-full max-w-4xl mb-12">
        <h1 className="text-3xl font-bold mb-4">전략 리포트</h1>
        <p className="text-gray-600 text-base">
          Intrix가 자동 생성한 전략 기획안입니다. 감정 흐름 → 욕구 분석 →
          전략 설계 → 포지셔닝까지 모든 단계를 포함하고 있으며, 최종 결과는
          Claude가 포맷팅한 리포트입니다.
        </p>
      </section>

      <section className="w-full max-w-4xl space-y-8">
        <Card>
          <CardHeader>
            <CardTitle>감정 분석</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-700">[감정 분석 결과 표시 영역]</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>핵심 욕구</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-700">[욕구 분석 결과 표시 영역]</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>전략 요약</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-700">[전략 요약 내용 표시 영역]</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>브랜딩 전략</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-700">[브랜딩 전략 결과 표시 영역]</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>카피라이팅 결과</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-700">[카피라이팅 결과 표시 영역]</p>
          </CardContent>
        </Card>
      </section>
    </main>
  );
} 