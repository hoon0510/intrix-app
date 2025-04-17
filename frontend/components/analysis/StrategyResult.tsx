"use client";

import React from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

interface StrategyResultProps {
  title: string;
  summary: string;
  slogans: string[];
}

const StrategyResult = ({ title, summary, slogans }: StrategyResultProps) => {
  return (
    <Card className="w-full mt-6">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="mb-4 text-sm text-gray-700">{summary}</p>
        <div className="space-y-2">
          {slogans.map((slogan, index) => (
            <div key={index} className="text-sm px-4 py-2 bg-muted rounded">
              {slogan}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default StrategyResult; 