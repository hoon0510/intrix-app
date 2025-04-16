"use client";

import React from "react";
import Link from "next/link";
import Layout from "@/components/layout";

export default function HomePage() {
  return (
    <Layout>
      <div className="min-h-screen bg-white flex flex-col items-center justify-center px-6">
        <div className="max-w-3xl text-center">
          <h1 className="text-4xl font-bold mb-4">Intrix</h1>
          <p className="text-lg text-gray-600 mb-6">
            감정과 욕구를 읽고 전략으로 바꾸는 자동화 마케팅 시스템
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4 mt-6">
            <Link href="/analyze">
              <span className="bg-black text-white px-6 py-3 rounded-lg hover:bg-gray-800 cursor-pointer">
                지금 분석하기
              </span>
            </Link>
            <Link href="/about">
              <span className="border border-black text-black px-6 py-3 rounded-lg hover:bg-gray-100 cursor-pointer">
                Intrix 소개
              </span>
            </Link>
          </div>
        </div>
      </div>
    </Layout>
  );
} 