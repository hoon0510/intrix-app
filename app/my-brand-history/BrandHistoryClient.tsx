'use client';

import React from 'react';
import { useRouter } from 'next/navigation';

interface BrandStrategyItem {
  id: string;
  created_at: string;
  reference_point: string;
  positioning: string;
  frame_shift: string;
}

interface BrandHistoryClientProps {
  items: BrandStrategyItem[];
}

export default function BrandHistoryClient({ items }: BrandHistoryClientProps) {
  const router = useRouter();

  const handleViewDetails = (id: string) => {
    router.push(`/brand-result/${id}`);
  };

  const handleCopy = async (positioning: string) => {
    try {
      await navigator.clipboard.writeText(positioning);
      // TODO: Add toast notification for successful copy
      console.log('Copied to clipboard');
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8 text-center">
          브랜드 전략 이력
        </h1>
        
        <div className="space-y-4">
          {items.map((item) => (
            <div key={item.id} className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex justify-between items-start mb-4">
                <div className="text-sm text-gray-500">
                  {new Date(item.created_at).toLocaleDateString('ko-KR', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleViewDetails(item.id)}
                    className="text-sm text-blue-600 hover:text-blue-800"
                  >
                    상세 보기
                  </button>
                  <button
                    onClick={() => handleCopy(item.positioning)}
                    className="text-sm text-gray-600 hover:text-gray-800"
                  >
                    복사
                  </button>
                </div>
              </div>
              
              <div className="space-y-2">
                <div>
                  <h3 className="text-sm font-semibold text-gray-600 mb-1">
                    레퍼런스 포인트
                  </h3>
                  <p className="text-gray-900">
                    {item.reference_point}
                  </p>
                </div>
                
                <div>
                  <h3 className="text-sm font-semibold text-gray-600 mb-1">
                    포지셔닝
                  </h3>
                  <p className="text-lg font-bold text-blue-600">
                    {item.positioning}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
} 