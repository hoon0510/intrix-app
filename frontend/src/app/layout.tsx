import "./globals.css";
import type { Metadata } from "next";
import { ReactNode } from "react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "Intrix – 전략 자동화 분석기",
  description: "감정 기반 전략을 자동으로 분석하고 실행 가능한 전략 리포트를 제공합니다.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ko">
      <body className="min-h-screen flex flex-col bg-white text-gray-900 dark:bg-neutral-900 dark:text-white">
        <Header />
        <main className="flex-1 pt-16 px-4">{children}</main>
        <Footer />
      </body>
    </html>
  );
} 