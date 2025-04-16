"use client";

import Layout from "@/components/layout";
import Link from "next/link";

export default function HomePage() {
  return (
    <Layout>
      <section className="flex flex-col items-center justify-center h-[calc(100vh-160px)] px-6 text-center">
        <h1 className="text-4xl font-bold mb-4">본능을 읽고, 전략을 설계하다</h1>
        <p className="text-lg text-gray-600 max-w-xl mb-6">
          INTRIX는 감정과 욕구를 기반으로 전략과 카피를 자동 생성하는 AI 전략 자동화 플랫폼입니다.
        </p>
        <Link
          href="/analyze"
          className="px-6 py-3 bg-black text-white rounded-xl text-sm font-medium hover:bg-gray-800 transition"
        >
          지금 바로 분석 시작하기
        </Link>
      </section>
    </Layout>
  );
} 