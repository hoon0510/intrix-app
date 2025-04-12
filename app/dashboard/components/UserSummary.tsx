import React from 'react';

interface UserSummaryProps {
  totalAnalyses: number;
  credits: number;
  lastAnalysis: string | null;
}

export default function UserSummary({
  totalAnalyses,
  credits,
  lastAnalysis,
}: UserSummaryProps) {
  const formatDate = (dateString: string | null) => {
    if (!dateString) return '없음';
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-5 border-b border-gray-200">
        <h2 className="text-lg font-medium text-gray-900">사용자 요약</h2>
      </div>
      <div className="p-6 space-y-6">
        <div>
          <h3 className="text-sm font-medium text-gray-500">총 분석 횟수</h3>
          <p className="mt-1 text-2xl font-semibold text-gray-900">
            {totalAnalyses}회
          </p>
        </div>
        <div>
          <h3 className="text-sm font-medium text-gray-500">보유 크레딧</h3>
          <p className="mt-1 text-2xl font-semibold text-gray-900">
            {credits.toLocaleString()} 크레딧
          </p>
        </div>
        <div>
          <h3 className="text-sm font-medium text-gray-500">최근 분석 일시</h3>
          <p className="mt-1 text-lg text-gray-900">
            {formatDate(lastAnalysis)}
          </p>
        </div>
      </div>
    </div>
  );
} 