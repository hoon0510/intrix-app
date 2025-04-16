import "./globals.css";
import { ReactNode } from "react";
import { Providers } from "./providers";

export const metadata = {
  title: "Intrix",
  description: "AI 기반 욕구 분석 전략 자동화 툴",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ko">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
} 