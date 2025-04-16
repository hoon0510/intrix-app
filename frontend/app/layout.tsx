import "@/app/globals.css";
import { ReactNode } from "react";

export const metadata = {
  title: "Intrix | 본능을 읽는 전략",
  description: "감정과 욕구 기반 전략 자동화 플랫폼",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ko">
      <body className="bg-white text-gray-900">
        {children}
      </body>
    </html>
  );
} 