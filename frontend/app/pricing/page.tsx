"use client";

import Layout from "@/components/layout/Layout";

export default function PricingPage() {
  return (
    <Layout>
      <div className="max-w-6xl mx-auto py-20 px-6">
        <h1 className="text-4xl font-bold text-center mb-12">요금제 안내</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Free Plan */}
          <div className="border rounded-lg p-8">
            <h2 className="text-2xl font-semibold mb-4">Free</h2>
            <p className="text-3xl font-bold mb-6">₩0</p>
            <ul className="space-y-3 mb-8">
              <li>• 기본 분석 기능</li>
              <li>• 월 5회 무료 분석</li>
              <li>• 기본 리포트 제공</li>
            </ul>
            <button className="w-full py-2 bg-gray-100 rounded hover:bg-gray-200">
              시작하기
            </button>
          </div>

          {/* Pro Plan */}
          <div className="border rounded-lg p-8 bg-black text-white">
            <h2 className="text-2xl font-semibold mb-4">Pro</h2>
            <p className="text-3xl font-bold mb-6">₩29,900</p>
            <ul className="space-y-3 mb-8">
              <li>• 무제한 분석</li>
              <li>• 상세 리포트 제공</li>
              <li>• 우선 지원</li>
              <li>• API 액세스</li>
            </ul>
            <button className="w-full py-2 bg-white text-black rounded hover:bg-gray-100">
              업그레이드
            </button>
          </div>

          {/* Enterprise Plan */}
          <div className="border rounded-lg p-8">
            <h2 className="text-2xl font-semibold mb-4">Enterprise</h2>
            <p className="text-3xl font-bold mb-6">문의</p>
            <ul className="space-y-3 mb-8">
              <li>• 맞춤형 솔루션</li>
              <li>• 전담 매니저</li>
              <li>• SLA 보장</li>
              <li>• 기술 지원</li>
            </ul>
            <button className="w-full py-2 bg-gray-100 rounded hover:bg-gray-200">
              문의하기
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
} 