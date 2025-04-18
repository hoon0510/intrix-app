"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { dummyStrategy } from "@/lib/dummy";
console.log("dummyStrategy:", dummyStrategy);


export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-4xl mx-auto p-6 space-y-6">
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-gray-900">
              {dummyStrategy.title}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-base text-gray-700 mb-6 leading-relaxed">
              {dummyStrategy.summary}
            </p>
            <ul className="list-disc pl-6 text-gray-800 space-y-2">
              {dummyStrategy.slogans.map((slogan, idx) => (
                <li key={idx} className="text-base">
                  {slogan}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
} 