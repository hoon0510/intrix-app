import React from 'react';
import { notFound } from 'next/navigation';
import ShareClient from './ShareClient';

async function getAnalysisData(analysisId: string) {
  try {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/analysis/${analysisId}`,
      {
        cache: 'no-store' // Ensure fresh data for each request
      }
    );

    if (!response.ok) {
      if (response.status === 404) {
        notFound();
      }
      throw new Error('Failed to fetch analysis data');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching analysis data:', error);
    throw error;
  }
}

export default async function SharePage({
  params,
}: {
  params: { analysis_id: string };
}) {
  try {
    const analysisData = await getAnalysisData(params.analysis_id);
    return <ShareClient data={analysisData} />;
  } catch (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            분석 결과를 불러오는데 실패했습니다
          </h1>
          <p className="text-gray-600">
            잠시 후 다시 시도해주세요.
          </p>
        </div>
      </div>
    );
  }
} 