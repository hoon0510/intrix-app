"use client";

import React from "react";
import Layout from "@/components/layout";

export default function PricingPage() {
  return (
    <Layout>
      <div className="min-h-screen bg-white px-6 py-12 flex flex-col items-center">
        <div className="max-w-3xl text-center">
          <h1 className="text-3xl font-bold mb-4">요금제 안내</h1>
          <p className="text-gray-700 mb-10">
            Intrix는 크레딧 기반으로 요금이 부과되며, 사용량에 따라 합리적으로 결제할 수 있습니다.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="border rounded-xl p-6 shadow-md">
              <h2 className="text-xl font-semibold mb-2">Lite</h2>
              <p className="text-gray-600 mb-4">₩7,900 / 500크레딧</p>
              <ul className="text-left text-gray-600 list-disc list-inside space-y-1 mb-4">
                <li>전략 분석 1회</li>
                <li>카피라이팅 포함</li>
                <li>결과 저장 가능</li>
              </ul>
            </div>
            <div className="border rounded-xl p-6 shadow-md">
              <h2 className="text-xl font-semibold mb-2">Standard</h2>
              <p className="text-gray-600 mb-4">₩29,900 / 2,000크레딧</p>
              <ul className="text-left text-gray-600 list-disc list-inside space-y-1 mb-4">
                <li>전략 분석 최대 7회</li>
                <li>PDF/HTML 다운로드</li>
                <li>즐겨찾기 기능 제공</li>
              </ul>
            </div>
            <div className="border rounded-xl p-6 shadow-md">
              <h2 className="text-xl font-semibold mb-2">Pro</h2>
              <p className="text-gray-600 mb-4">₩119,900 / 10,000크레딧</p>
              <ul className="text-left text-gray-600 list-disc list-inside space-y-1 mb-4">
                <li>전략 분석 무제한</li>
                <li>퍼포먼스 설계 보고서 포함</li>
                <li>관리자 패널 기능</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
} 