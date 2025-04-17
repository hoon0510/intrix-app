"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

export default function HomeHero() {
  const router = useRouter();

  return (
    <section className="w-full py-12 md:py-24 lg:py-32 bg-white">
      <div className="container px-4 md:px-6">
        <div className="flex flex-col items-center space-y-4 text-center">
          <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl">
            감정과 욕구 기반<br />전략 자동화 도구
          </h1>
          <p className="mx-auto max-w-[700px] text-gray-500 md:text-xl">
            고객의 감정과 욕구를 분석하여 최적의 전략과 카피를 자동으로 생성합니다.
          </p>
          <Button
            size="lg"
            className="mt-6 px-8 py-6 text-lg font-semibold rounded-xl bg-primary hover:bg-primary/90 transition-colors"
            onClick={() => router.push("/analyze")}
          >
            지금 바로 분석 시작하기
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
        </div>
      </div>
    </section>
  );
} 