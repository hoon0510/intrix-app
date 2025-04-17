"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { useRouter } from "next/navigation";

export default function AnalyzerPage() {
  const [marketType, setMarketType] = useState<"existing" | "new" | null>(null);
  const [feedbackList, setFeedbackList] = useState<string[]>([""]);
  const [useCrawling, setUseCrawling] = useState(false);
  const router = useRouter();

  const addFeedbackField = () => {
    if (feedbackList.length >= 200) return;
    setFeedbackList([...feedbackList, ""]);
  };

  const updateFeedback = (index: number, value: string) => {
    const updated = [...feedbackList];
    updated[index] = value;
    setFeedbackList(updated);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const formData = new FormData(e.target as HTMLFormElement);
    const payload: any = {
      market_type: marketType,
      item_name: formData.get("item_name"),
      service_definition: formData.get("service_definition"),
      target_audience: formData.get("target_audience"),
      usage_scenario: formData.get("usage_scenario"),
      desired_positioning: formData.get("desired_positioning"),
    };

    if (marketType === "existing") {
      if (useCrawling) {
        const selectedChannels = formData.getAll("channels");
        payload.crawl_channels = selectedChannels;
      } else {
        payload.customer_feedback = feedbackList.filter((f) => f.trim() !== "");
      }
    }

    const res = await fetch("/api/analysis", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    router.push(`/result/${data.job_id}`);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-10 space-y-6">
      <h1 className="text-2xl font-bold">전략 분석 시작</h1>

      {/* 진입 유형 선택 */}
      <div className="space-x-4">
        <Button variant={marketType === "existing" ? "default" : "outline"} onClick={() => setMarketType("existing")}>
          기존시장 진입
        </Button>
        <Button variant={marketType === "new" ? "default" : "outline"} onClick={() => setMarketType("new")}>
          신시장 진입
        </Button>
      </div>

      {marketType && (
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* 공통 입력 */}
          <Field label="아이템명" name="item_name" />
          <Field label="서비스 정의" name="service_definition" textarea />
          <Field label="핵심 타겟" name="target_audience" />
          <Field label="사용상황 시나리오" name="usage_scenario" textarea />
          <Field label="목표 포지셔닝" name="desired_positioning" textarea />

          {/* 기존시장 전용 입력 */}
          {marketType === "existing" && (
            <>
              <div className="space-y-2">
                <Label>고객 반응 입력 방식</Label>
                <div className="flex items-center space-x-4">
                  <Button
                    type="button"
                    variant={!useCrawling ? "default" : "outline"}
                    onClick={() => setUseCrawling(false)}
                  >
                    직접 입력
                  </Button>
                  <Button
                    type="button"
                    variant={useCrawling ? "default" : "outline"}
                    onClick={() => setUseCrawling(true)}
                  >
                    크롤링 사용
                  </Button>
                </div>
              </div>

              {!useCrawling ? (
                <div className="space-y-2">
                  <Label>고객 반응 입력 (최대 200개)</Label>
                  {feedbackList.map((text, idx) => (
                    <Input
                      key={idx}
                      value={text}
                      onChange={(e) => updateFeedback(idx, e.target.value)}
                      className="mb-2"
                      placeholder={`고객 반응 ${idx + 1}`}
                    />
                  ))}
                  <Button type="button" variant="outline" onClick={addFeedbackField}>
                    + 반응 추가
                  </Button>
                </div>
              ) : (
                <div className="space-y-2">
                  <Label>크롤링 대상 채널</Label>
                  <div className="grid grid-cols-2 gap-2">
                    {["reddit", "ppomppu", "dcinside", "fmkorea", "instagram", "youtube"].map((channel) => (
                      <label key={channel} className="flex items-center space-x-2">
                        <input type="checkbox" name="channels" value={channel} />
                        <span>{channel}</span>
                      </label>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}

          <Button type="submit">분석 요청</Button>
        </form>
      )}
    </div>
  );
}

function Field({ label, name, textarea }: { label: string; name: string; textarea?: boolean }) {
  return (
    <div className="space-y-2">
      <Label htmlFor={name}>{label}</Label>
      {textarea ? (
        <Textarea id={name} name={name} required rows={4} />
      ) : (
        <Input id={name} name={name} required />
      )}
    </div>
  );
} 