import React from 'react';
import { FeedbackStats } from '@/components/FeedbackStats';

interface AnalysisCardProps {
  id: string;
  inputText: string;
  copy: string;
  createdAt: string;
}

export default function AnalysisCard({
  id,
  inputText,
  copy,
  createdAt,
}: AnalysisCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="space-y-4">
        <div className="flex justify-between items-start">
          <div>
            <p className="text-sm text-gray-500">
              {new Date(createdAt).toLocaleString()}
            </p>
            <p className="mt-1 text-sm text-gray-600">{inputText}</p>
          </div>
        </div>
        
        <div className="mt-4">
          <p className="text-lg font-medium text-gray-900">{copy}</p>
          <FeedbackStats analysisId={id} />
        </div>
      </div>
    </div>
  );
} 