import React from 'react';

interface ShareData {
  positioning: string;
  copy: string;
  style: string;
  report_html: string;
}

interface ShareClientProps {
  data: ShareData;
}

export default function ShareClient({ data }: ShareClientProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Positioning */}
        <h1 className="text-3xl font-bold text-center text-gray-900 mb-8">
          {data.positioning}
        </h1>

        {/* Copy with Style */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <div className="prose prose-lg max-w-none">
            <div className="text-xl text-gray-900 mb-2">{data.copy}</div>
            <div className="text-sm text-gray-500">스타일: {data.style}</div>
          </div>
        </div>

        {/* Report HTML */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div 
            className="prose prose-lg max-w-none"
            dangerouslySetInnerHTML={{ __html: data.report_html }}
          />
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>이 분석은 Intrix를 통해 생성되었습니다.</p>
        </div>
      </div>
    </div>
  );
} 