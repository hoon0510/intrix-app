'use client';

import React from 'react';
import { useRouter } from 'next/navigation';

interface FullReportData {
  report_html: string;
  copy: string;
  style: string;
  reference_point: string;
  frame_shift: string;
  positioning: string;
}

interface FullReportClientProps {
  data: FullReportData;
}

export default function FullReportClient({ data }: FullReportClientProps) {
  const router = useRouter();

  const handleDownloadPDF = async () => {
    try {
      const response = await fetch('/api/download-report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Failed to download PDF');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'marketing-strategy-report.pdf';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading PDF:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            마케팅 전략 리포트
          </h1>
          <button
            onClick={handleDownloadPDF}
            className="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            PDF 다운로드
          </button>
        </div>

        {/* Brand Strategy Section */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            브랜드 전략
          </h2>
          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-semibold text-gray-600 mb-1">
                포지셔닝
              </h3>
              <p className="text-2xl font-bold text-blue-600">
                {data.positioning}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-600 mb-1">
                레퍼런스 포인트
              </h3>
              <p className="text-lg text-gray-900">
                {data.reference_point}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-600 mb-1">
                프레임 시프트
              </h3>
              <p className="text-lg text-gray-900">
                {data.frame_shift}
              </p>
            </div>
          </div>
        </div>

        {/* Copy Section */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            마케팅 카피
          </h2>
          <div className="space-y-2">
            <p className="text-lg font-medium text-gray-900">
              {data.copy}
            </p>
            <p className="text-sm text-gray-500">
              스타일: {data.style}
            </p>
          </div>
        </div>

        {/* Strategy Report Section */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            전략 리포트
          </h2>
          <div 
            className="prose prose-sm max-w-none"
            dangerouslySetInnerHTML={{ __html: data.report_html }}
          />
        </div>
      </div>
    </div>
  );
} 