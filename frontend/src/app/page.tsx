"use client";

import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();

  return (
    <div className="max-w-6xl mx-auto px-6 py-20 space-y-20">
      
      {/* Hero Section */}
      <section className="text-center space-y-4">
        <h1 className="text-4xl md:text-5xl font-bold leading-tight">
          감정과 욕구 기반<br />전략 자동화 시스템
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300">
          고객의 언어에서 욕구를 감지하고, 전환 전략을 자동으로 생성하세요.
        </p>
        <Button onClick={() => router.push("/analyzer")} size="lg">
          지금 분석 시작하기 →
        </Button>
      </section>

      {/* 기능 요약 Section */}
      <section className="grid md:grid-cols-3 gap-6">
        <FeatureCard
          title="AI 감정 분석"
          desc="리뷰·댓글 속 감정을 분석하여 상위/하위 욕구를 분해합니다."
        />
        <FeatureCard
          title="전략 자동 설계"
          desc="감정 흐름에 따라 GPT가 완성도 높은 전략을 자동 설계합니다."
        />
        <FeatureCard
          title="리포트 & PDF"
          desc="전략 리포트는 HTML과 PDF로 제공되며, 공유·저장 모두 가능합니다."
        />
      </section>

      {/* CTA Section */}
      <section className="text-center space-y-4">
        <h2 className="text-2xl font-semibold">Intrix는 누구를 위한 도구인가요?</h2>
        <p className="text-gray-600 dark:text-gray-300">
          전략 설계가 필요한 마케터, 기획자, 창업자 모두에게 강력한 전략 파트너가 되어줍니다.
        </p>
        <Button onClick={() => router.push("/analyzer")} size="lg" variant="outline">
          전략 분석 시작하기
        </Button>
      </section>
    </div>
  );
}

function FeatureCard({ title, desc }: { title: string; desc: string }) {
  return (
    <div className="border rounded-xl p-6 shadow-sm bg-white dark:bg-neutral-800">
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600 dark:text-gray-300">{desc}</p>
    </div>
  );
} 