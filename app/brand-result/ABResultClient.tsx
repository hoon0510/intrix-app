'use client';

import React from 'react';
import { useRouter } from 'next/navigation';

interface BrandStrategyResult {
  reference_point: string;
  frame_shift: string;
  positioning: string;
}

interface BrandResultClientProps {
  result: BrandStrategyResult;
}

export default function BrandResultClient({ result }: BrandResultClientProps) {
  const router = useRouter();

  const handleViewFullStrategy = () => {
    // TODO: Implement navigation to full strategy view
    console.log('View full strategy');
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8 text-center">
          브랜드 전략 결과
        </h1>
        
        <div className="space-y-6">
          {/* Positioning Card - Highlighted */}
          <div className="bg-white rounded-lg shadow-lg p-6 border-2 border-blue-500">
            <h2 className="text-sm font-semibold text-blue-600 mb-2">
              포지셔닝
            </h2>
            <p className="text-2xl font-bold text-gray-900 text-center">
              {result.positioning}
            </p>
          </div>
          
          {/* Reference Point Card */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-sm font-semibold text-gray-600 mb-2">
              레퍼런스 포인트
            </h2>
            <p className="text-lg text-gray-900">
              {result.reference_point}
            </p>
          </div>
          
          {/* Frame Shift Card */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-sm font-semibold text-gray-600 mb-2">
              프레임 시프트
            </h2>
            <p className="text-lg text-gray-900">
              {result.frame_shift}
            </p>
          </div>
          
          {/* View Full Strategy Button */}
          <button
            onClick={handleViewFullStrategy}
            className="w-full mt-6 bg-gray-900 text-white py-3 px-4 rounded-md hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
          >
            전략 전체 다시 보기
          </button>
        </div>
      </div>
    </div>
  );
} 