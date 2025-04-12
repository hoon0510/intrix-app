'use client';

import React, { useState } from "react";
import ShareButton from "@/app/components/ShareButton";

interface Variant {
  id: string;
  copy: string;
  style: string;
  report_html: string;
}

interface ABResultClientProps {
  variantA: Variant;
  variantB: Variant;
}

export default function ABResultClient({ variantA, variantB }: ABResultClientProps) {
  const [selectedVariant, setSelectedVariant] = useState<Variant | null>(null);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-bold text-gray-900">A/B 테스트 결과</h1>
          {selectedVariant && (
            <ShareButton analysisId={selectedVariant.id} />
          )}
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div 
            className="bg-white rounded-lg shadow p-6 cursor-pointer hover:shadow-lg transition-shadow"
            onClick={() => setSelectedVariant(variantA)}
          >
            <h2 className="text-xl font-semibold mb-4">변형 A</h2>
            <div dangerouslySetInnerHTML={{ __html: variantA.report_html }} />
          </div>
          
          <div 
            className="bg-white rounded-lg shadow p-6 cursor-pointer hover:shadow-lg transition-shadow"
            onClick={() => setSelectedVariant(variantB)}
          >
            <h2 className="text-xl font-semibold mb-4">변형 B</h2>
            <div dangerouslySetInnerHTML={{ __html: variantB.report_html }} />
          </div>
        </div>
      </div>
    </div>
  );
} 