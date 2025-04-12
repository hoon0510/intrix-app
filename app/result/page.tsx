'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import html2pdf from 'html2pdf.js';

interface ResultPageProps {
  report_html: string;
  copy: string;
  style: string;
  final_credit: number;
}

export default function ResultPage({ report_html, copy, style, final_credit }: ResultPageProps) {
  const router = useRouter();
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  const handleDownloadPDF = () => {
    const element = document.getElementById('report-content');
    if (element) {
      const opt = {
        margin: 1,
        filename: 'marketing-strategy-report.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
      };
      html2pdf().from(element).set(opt).save();
    }
  };

  const handleReanalyze = () => {
    router.push('/');
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Marketing Strategy Report</h1>
          <p className="mt-2 text-sm text-gray-600">
            Credits used: <span className="font-semibold">{final_credit}</span>
          </p>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Report Section */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">Analysis Report</h2>
              <div 
                id="report-content"
                className="prose max-w-none"
                dangerouslySetInnerHTML={{ __html: report_html }}
              />
            </div>
          </div>

          {/* Copy Section */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">Generated Copy</h2>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-500 mb-2">Style: {style}</p>
                <p className="text-gray-700 whitespace-pre-wrap">{copy}</p>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="mt-6 space-y-4">
              <button
                onClick={handleDownloadPDF}
                className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Download PDF
              </button>
              <button
                onClick={handleReanalyze}
                className="w-full bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors"
              >
                Analyze Again
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 