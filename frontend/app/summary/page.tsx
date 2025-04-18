"use client";

import Layout from "@/components/layout/Layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function SummaryPage() {
  return (
    <Layout>
      <div className="max-w-4xl mx-auto py-20 px-6">
        <h1 className="text-3xl font-bold mb-8">분석 요약</h1>
        <div className="grid gap-6">
          <Card>
            <CardHeader>
              <CardTitle>최근 분석 결과</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">아직 분석 결과가 없습니다.</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </Layout>
  );
} 