import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useRouter } from "next/navigation";
import { Skeleton } from "@/components/ui/skeleton";

export default function AnalyzeForm() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!text.trim()) return;

    setLoading(true);
    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error("분석 요청에 실패했습니다.");
      }

      const data = await response.json();
      router.push(`/analyze/result?id=${data.id}`);
    } catch (error) {
      console.error("Error:", error);
      alert("분석 요청 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="분석할 텍스트를 입력하세요..."
        className="min-h-[200px]"
        disabled={loading}
      />
      {loading ? (
        <Skeleton className="h-10 w-full" />
      ) : (
        <Button type="submit" className="w-full" disabled={loading}>
          분석 요청
        </Button>
      )}
    </form>
  );
} 