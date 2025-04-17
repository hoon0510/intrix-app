import "./globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Navbar from "@/components/ui/navbar";
import Footer from "@/components/Footer";
import { ReactNode } from "react";
import Header from "@/components/Header";
import { ThemeProvider } from "@/components/theme-provider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Intrix – 전략 자동화 분석기",
  description: "AI 감정 분석과 욕구 기반 전략 자동화를 통해 실행 가능한 브랜드 전략을 만드세요.",
  keywords: ["Intrix", "전략 자동화", "AI 분석기", "감정 분석", "브랜드 전략"],
  openGraph: {
    title: "Intrix – 전략 자동화 분석기",
    description: "AI 감정 분석과 욕구 기반 전략 자동화 시스템",
    url: "https://your-intrix-domain.com",
    siteName: "Intrix",
    images: [
      {
        url: "https://your-intrix-domain.com/og-default.png",
        width: 1200,
        height: 630,
        alt: "Intrix Preview",
      },
    ],
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Intrix – 전략 자동화 분석기",
    description: "AI 감정 분석과 욕구 기반 전략 자동화 시스템",
    images: ["https://your-intrix-domain.com/og-default.png"],
  },
};

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="ko" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <Header />
          <main className="flex-1">{children}</main>
          <Footer />
        </ThemeProvider>
      </body>
    </html>
  );
} 