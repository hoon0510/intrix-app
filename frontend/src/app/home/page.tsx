"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function Home() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const formData = new FormData(e.target as HTMLFormElement);
      const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("분석 요청 실패");
      }

      const data = await response.json();
      router.push(`/result/${data.id}`);
    } catch (error) {
      console.error("Error:", error);
      alert("분석 중 오류가 발생했습니다. 다시 시도해주세요.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">브랜드 전략 분석</h1>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="keyword">키워드</Label>
            <Input
              id="keyword"
              name="keyword"
              placeholder="분석할 키워드를 입력하세요"
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="context">맥락</Label>
            <Textarea
              id="context"
              name="context"
              placeholder="키워드에 대한 추가 맥락을 설명해주세요"
              rows={4}
            />
          </div>

          <Button type="submit" disabled={isLoading}>
            {isLoading ? "분석 중..." : "분석 시작"}
          </Button>
        </form>

        <div className="mt-12 grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>감정 분석</CardTitle>
              <CardDescription>고객의 감정을 AI로 분석</CardDescription>
            </CardHeader>
            <CardContent>
              <p>고객의 감정을 정확하게 파악하여 브랜드 전략에 반영합니다.</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>전략 제안</CardTitle>
              <CardDescription>데이터 기반 전략 수립</CardDescription>
            </CardHeader>
            <CardContent>
              <p>분석 결과를 바탕으로 효과적인 브랜드 전략을 제안합니다.</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
} 