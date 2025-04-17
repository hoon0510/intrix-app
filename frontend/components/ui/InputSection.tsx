"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useRouter } from "next/navigation";

export default function InputSection() {
  const [input, setInput] = useState("");
  const router = useRouter();

  const isValid = input.length >= 3;

  const handleSubmit = () => {
    if (isValid) {
      // TODO: API 호출 로직 추가
      router.push("/analyze/result");
    }
  };

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <Textarea
          placeholder="브랜드나 제품에 대한 키워드를 입력해주세요..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="min-h-[100px]"
        />
        {!isValid && input.length > 0 && (
          <p className="text-sm text-red-500 mt-2">
            최소 3자 이상의 키워드를 입력해주세요.
          </p>
        )}
      </div>
      <Button 
        disabled={!isValid} 
        onClick={handleSubmit}
        className="w-full"
      >
        분석하기
      </Button>
    </div>
  );
} 