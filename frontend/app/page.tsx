"use client";

import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-6 text-center">
      <h1 className="text-4xl md:text-6xl font-bold mb-6 tracking-tight">
        본능을 읽고, 전략을 자동화하다
      </h1>
      <p className="text-lg md:text-xl mb-8 max-w-2xl text-gray-600">
        Intrix는 고객의 감정과 욕구를 기반으로<br className="hidden md:inline" />
        전략과 카피를 자동 설계하는 AI 전략 자동화 플랫폼입니다.
      </p>
      <Link
        href="/analyze"
        className="px-6 py-3 bg-black text-white rounded-xl text-lg font-semibold hover:bg-gray-800 transition"
      >
        지금 바로 전략 분석 시작하기
      </Link>
    </main>
  );
} 