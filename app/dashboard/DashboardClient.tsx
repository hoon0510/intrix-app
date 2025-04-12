import React from 'react';
import UserSummary from './components/UserSummary';
import AnalysisCard from './components/AnalysisCard';

interface DashboardData {
  user: {
    total_analyses: number;
    credits: number;
    last_analysis: string | null;
  };
  recentAnalyses: Array<{
    id: string;
    input_text: string;
    copy: string;
    created_at: string;
  }>;
}

interface DashboardClientProps {
  data: DashboardData;
}

export default function DashboardClient({ data }: DashboardClientProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - User Summary */}
          <div className="lg:col-span-1">
            <UserSummary
              totalAnalyses={data.user.total_analyses}
              credits={data.user.credits}
              lastAnalysis={data.user.last_analysis}
            />
          </div>

          {/* Right Column - Recent Analyses */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow">
              <div className="px-6 py-5 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">
                  최근 분석 결과
                </h2>
              </div>
              <div className="p-6 space-y-6">
                {data.recentAnalyses.map((analysis) => (
                  <AnalysisCard
                    key={analysis.id}
                    id={analysis.id}
                    inputText={analysis.input_text}
                    copy={analysis.copy}
                    createdAt={analysis.created_at}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 