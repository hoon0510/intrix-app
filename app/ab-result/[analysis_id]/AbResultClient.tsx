'use client';

import React from 'react';
import { FeedbackBox } from '@/components/FeedbackBox';

interface Analysis {
  id: string;
  // ... other analysis properties
}

interface AbResultClientProps {
  analysis: Analysis;
}

export function AbResultClient({ analysis }: AbResultClientProps) {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm p-6">
        {/* ... existing content ... */}
        
        <div className="mt-6 pt-4 border-t border-gray-100">
          <FeedbackBox analysisId={analysis.id} />
        </div>
      </div>
    </div>
  );
} 