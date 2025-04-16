import "./globals.css";
import { ReactNode } from "react";
import { Providers } from "./providers";

export const metadata = {
  title: "Intrix - 욕구 기반 전략 자동화",
  description: "감정과 욕구 흐름을 기반으로 전략을 자동 설계하는 AI 플랫폼",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ko">
      <head />
      <body className="bg-white text-gray-900 min-h-screen">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
} 