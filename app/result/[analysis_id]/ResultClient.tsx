'use client';

import React from 'react';
import { FeedbackBox } from '@/components/FeedbackBox';

interface Analysis {
  id: string;
  // ... other analysis properties
}

interface BrandStrategy {
  // ... brand strategy properties
}

interface ResultClientProps {
  analysis: Analysis;
  brandStrategy: BrandStrategy;
}

export function ResultClient({ analysis, brandStrategy }: ResultClientProps) {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="mt-6 pt-4 border-t border-gray-100">
          <FeedbackBox analysisId={analysis.id} />
        </div>
      </div>
    </div>
  );
} 