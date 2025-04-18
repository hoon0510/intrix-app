"use client";

import React, { useState } from "react";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";

export default function AnalyzePage() {
  const [selectedTab, setSelectedTab] = useState("new");
  const [inputText, setInputText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleTabChange = (value: string) => {
    setSelectedTab(value);
    setInputText("");
    setResult(null);
  };

  const handleAnalyze = async () => {
    if (!inputText.trim()) {
      toast.error("분석할 텍스트를 입력해주세요.");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("/api/analyze/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: inputText,
          analysis_type: selectedTab,
        }),
      });

      if (!response.ok) {
        throw new Error("분석 중 오류가 발생했습니다.");
      }

      const data = await response.json();
      setResult(data.analysis);
      toast.success("분석이 완료되었습니다.");
    } catch (error) {
      console.error("Analysis error:", error);
      toast.error("분석 중 오류가 발생했습니다. 다시 시도해주세요.");
    } finally {
      setLoading(false);
    }
  };

  const renderResult = () => {
    if (!result) return null;

    return (
      <div className="mt-4 p-4 bg-gray-50 rounded-lg">
        {Object.entries(result).map(([key, value]) => (
          <div key={key} className="mb-4">
            <h3 className="font-semibold text-lg mb-2">{key}</h3>
            {Array.isArray(value) ? (
              <ul className="list-disc pl-5">
                {value.map((item, index) => (
                  <li key={index}>{String(item)}</li>
                ))}
              </ul>
            ) : (
              <p>{String(value)}</p>
            )}
          </div>
        ))}
      </div>
    );
  };

  return (
    <main className="p-8">
      <Tabs defaultValue="new" onValueChange={handleTabChange} className="w-full">
        <TabsList>
          <TabsTrigger value="new">신규유입 분석</TabsTrigger>
          <TabsTrigger value="retention">리텐션 분석</TabsTrigger>
          <TabsTrigger value="desire">다층 욕구 분석</TabsTrigger>
          <TabsTrigger value="report">리포트형 분석</TabsTrigger>
        </TabsList>

        <TabsContent value="new">
          <Card>
            <CardHeader>
              <CardTitle>신규유입 분석</CardTitle>
              <CardDescription>소비자 초기 반응을 분석합니다.</CardDescription>
            </CardHeader>
            <CardContent>
              <Input 
                placeholder="텍스트를 입력하세요..." 
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
              />
              {renderResult()}
            </CardContent>
            <CardFooter>
              <Button 
                onClick={handleAnalyze} 
                disabled={loading}
              >
                {loading ? "분석 중..." : "분석 시작"}
              </Button>
            </CardFooter>
          </Card>
        </TabsContent>

        <TabsContent value="retention">
          <Card>
            <CardHeader>
              <CardTitle>리텐션 분석</CardTitle>
              <CardDescription>지속 이용자 패턴을 분석합니다.</CardDescription>
            </CardHeader>
            <CardContent>
              <Input 
                placeholder="리텐션 분석 텍스트 입력..." 
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
              />
              {renderResult()}
            </CardContent>
            <CardFooter>
              <Button 
                onClick={handleAnalyze} 
                disabled={loading}
              >
                {loading ? "분석 중..." : "분석 시작"}
              </Button>
            </CardFooter>
          </Card>
        </TabsContent>

        <TabsContent value="desire">
          <Card>
            <CardHeader>
              <CardTitle>다층 욕구 분석</CardTitle>
              <CardDescription>심층적인 욕구 구조를 해석합니다.</CardDescription>
            </CardHeader>
            <CardContent>
              <Input 
                placeholder="욕구 분석 텍스트 입력..." 
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
              />
              {renderResult()}
            </CardContent>
            <CardFooter>
              <Button 
                onClick={handleAnalyze} 
                disabled={loading}
              >
                {loading ? "분석 중..." : "분석 시작"}
              </Button>
            </CardFooter>
          </Card>
        </TabsContent>

        <TabsContent value="report">
          <Card>
            <CardHeader>
              <CardTitle>리포트형 분석</CardTitle>
              <CardDescription>전문가용 전략 보고서 분석</CardDescription>
            </CardHeader>
            <CardContent>
              <Input 
                placeholder="보고서용 텍스트 입력..." 
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
              />
              {renderResult()}
            </CardContent>
            <CardFooter>
              <Button 
                onClick={handleAnalyze} 
                disabled={loading}
              >
                {loading ? "분석 중..." : "리포트 생성"}
              </Button>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>
    </main>
  );
} 