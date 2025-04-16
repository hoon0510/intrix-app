// frontend/pages/index.tsx
// intrix-ui-design.tsx 내용을 기반으로 복사한 UI 코드입니다

"use client";

import React, { useState } from "react";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "../components/ui/tabs";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { Input } from "../components/ui/input";

export default function AnalyzePage() {
  const [selectedTab, setSelectedTab] = useState("new");
  const handleTabChange = (value: string) => setSelectedTab(value);

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
              <Input placeholder="텍스트를 입력하세요..." />
            </CardContent>
            <CardFooter>
              <Button>분석 시작</Button>
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
              <Input placeholder="리텐션 분석 텍스트 입력..." />
            </CardContent>
            <CardFooter>
              <Button>분석 시작</Button>
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
              <Input placeholder="욕구 분석 텍스트 입력..." />
            </CardContent>
            <CardFooter>
              <Button>분석 시작</Button>
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
              <Input placeholder="보고서용 텍스트 입력..." />
            </CardContent>
            <CardFooter>
              <Button>리포트 생성</Button>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>
    </main>
  );
}
