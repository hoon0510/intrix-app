"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface StrategySummaryProps {
  summary: string;
  slogans: string[];
}

export default function StrategySummary({ summary, slogans }: StrategySummaryProps) {
  return (
    <Card className="w-full mt-4">
      <CardHeader>
        <CardTitle>전략 요약</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="mb-4 text-base leading-relaxed">{summary}</p>
        <ul className="list-disc list-inside text-sm space-y-1">
          {slogans.map((slogan, index) => (
            <li key={index} className="text-muted-foreground">"{slogan}"</li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
} 