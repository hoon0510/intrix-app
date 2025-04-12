'use client';

import React, { useEffect, useState } from 'react';

interface FeedbackStatsProps {
  analysisId: string;
}

interface FeedbackSummary {
  positive: number;
  negative: number;
}

export function FeedbackStats({ analysisId }: FeedbackStatsProps) {
  const [stats, setStats] = useState<FeedbackSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch(`/api/feedback/summary/${analysisId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch feedback stats');
        }
        const data = await response.json();
        setStats(data);
      } catch (err) {
        setError('피드백 통계를 불러오는데 실패했습니다');
        console.error('Error fetching feedback stats:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchStats();
  }, [analysisId]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-4">
        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-sm text-red-500 p-4">
        {error}
      </div>
    );
  }

  if (!stats) {
    return null;
  }

  return (
    <div className="mt-4 p-4 bg-gray-50 rounded-lg">
      <div className="flex items-center justify-center gap-6">
        <div className="flex items-center gap-2">
          <span className="text-2xl">👍</span>
          <span className="text-gray-700 font-medium">{stats.positive}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-2xl">👎</span>
          <span className="text-gray-700 font-medium">{stats.negative}</span>
        </div>
      </div>
    </div>
  );
} 