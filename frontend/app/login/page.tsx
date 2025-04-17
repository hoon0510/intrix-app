"use client";

import { signIn } from "next-auth/react";
import { Button } from "@/components/ui/button";

export default function LoginPage() {
  return (
    <div className="min-h-screen flex flex-col justify-center items-center px-4">
      <h1 className="text-2xl font-bold mb-4">로그인이 필요합니다</h1>
      <p className="text-gray-600 dark:text-gray-300 mb-6 text-center max-w-md">
        이 페이지에 접근하려면 Google 계정으로 로그인해야 합니다.
        Intrix는 분석 결과와 전략 데이터를 안전하게 보호합니다.
      </p>
      <Button onClick={() => signIn("google")} size="lg">
        Google로 로그인하기 →
      </Button>
    </div>
  );
} 