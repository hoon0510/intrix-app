"use client";

import React from "react";
import Layout from "@/components/layout";

export default function AboutPage() {
  return (
    <Layout>
      <div className="min-h-screen bg-white flex flex-col items-center justify-center px-6">
        <div className="max-w-2xl text-center">
          <h1 className="text-3xl font-bold mb-4">Intrix 소개</h1>
          <p className="text-lg text-gray-700 mb-6">
            Intrix는 고객의 감정과 욕구를 자동 분석하여 전략, 카피, 브랜딩까지 설계하는
            AI 기반 마케팅 자동화 시스템입니다. 단순한 데이터 요약이 아닌, 실제 전환과 실행을
            위한 전략 보고서를 제공합니다.
          </p>
          <ul className="text-left list-disc text-gray-600 px-4 space-y-2">
            <li>Claude를 통한 감정 및 욕구 분석</li>
            <li>GPT 기반 전략 설계 및 카피라이팅</li>
            <li>PDF, HTML 보고서 자동 생성</li>
            <li>정량화된 욕구 기반 KPI 정렬</li>
          </ul>
        </div>
      </div>
    </Layout>
  );
} 