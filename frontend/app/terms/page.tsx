import React from "react";

export default function TermsPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto px-4 py-12">
        <h1 className="text-2xl font-bold mb-6">이용약관</h1>
        <p className="mb-4 text-gray-600">
          본 약관은 Intrix 서비스를 이용함에 있어 필요한 사항을 규정합니다.
        </p>

        <section className="space-y-6">
          <div>
            <h2 className="text-xl font-semibold mb-2">1. 목적</h2>
            <p className="text-gray-600">
              Intrix는 고객 피드백을 분석하여 전략과 카피를 자동 생성하는 도구입니다.
            </p>
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-2">2. 책임과 면책</h2>
            <p className="text-gray-600">
              본 서비스는 자동 생성된 전략 및 콘텐츠에 대한 윤리적·법적 책임을 지지 않으며, 
              최종 판단은 사용자에게 있습니다.
            </p>
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-2">3. 지적재산권</h2>
            <p className="text-gray-600">
              Intrix가 제공하는 콘텐츠의 저작권은 본 서비스에 있으며, 
              무단 복제 및 배포를 금지합니다.
            </p>
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-2">4. 기타</h2>
            <p className="text-gray-600">
              본 약관은 사전 고지 없이 변경될 수 있으며, 
              변경 시 공지사항을 통해 고지됩니다.
            </p>
          </div>
        </section>
      </div>
    </div>
  );
} 