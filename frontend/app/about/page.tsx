"use client";

import React from "react";
import Layout from "@/components/layout";

export default function AboutPage() {
  return (
    <Layout>
      <div className="min-h-screen px-6 py-12 bg-white text-gray-800">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold mb-6">Intrix란?</h1>
          <p className="text-lg mb-6">
            Intrix는 무의식적 감정 흐름과 욕구 구조를 분석하여, 기존 마케팅 전략의 한계를 넘어서는 새로운 전략을 자동으로 생성하는 시스템입니다.
          </p>
          <h2 className="text-2xl font-semibold mb-4">왜 Intrix인가?</h2>
          <ul className="list-disc pl-5 space-y-2 mb-6">
            <li>전략가가 없어도 전략이 만들어집니다.</li>
            <li>감정, 욕구, 실행을 하나의 파이프라인으로 연결합니다.</li>
            <li>사용자의 무의식적 선택 흐름을 기반으로 설계되어 전환율을 극대화합니다.</li>
          </ul>
          <h2 className="text-2xl font-semibold mb-4">기술 기반</h2>
          <p className="mb-6">
            Claude 3.7 Sonnet과 GPT-4 모델을 병렬로 활용하며, 모든 전략 결과는 포맷팅 및 결과 분리를 통해 실행 가능한 보고서 형태로 제공됩니다.
          </p>
          <h2 className="text-2xl font-semibold mb-4">Intrix가 바꾸고자 하는 것</h2>
          <ul className="list-disc pl-5 space-y-2">
            <li>감에 의존하는 마케팅이 아닌, 구조에 의한 전략을 만듭니다.</li>
            <li>표면적인 분석이 아닌, 감정과 욕구의 흐름을 다층적으로 설계합니다.</li>
            <li>누구나 전략가처럼 행동할 수 있는 환경을 제공합니다.</li>
          </ul>
        </div>
      </div>
    </Layout>
  );
} 