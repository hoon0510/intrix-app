import React from 'react';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import FullReportClient from './FullReportClient';

async function getFullReport() {
  const cookieStore = cookies();
  const authToken = cookieStore.get('auth_token')?.value;

  if (!authToken) {
    redirect('/login');
  }

  try {
    // Get user ID from auth token
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/user/me`, {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to get user info');
    }

    const userData = await response.json();
    const userId = userData.id;

    // Get latest analysis result
    const analysisResponse = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/user/${userId}/history`,
      {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      }
    );

    if (!analysisResponse.ok) {
      throw new Error('Failed to get analysis history');
    }

    const analysisData = await analysisResponse.json();
    const latestAnalysis = analysisData.data[0];

    // Get brand strategy
    const brandResponse = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/user/${userId}/brand/${latestAnalysis.id}`,
      {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      }
    );

    if (!brandResponse.ok) {
      throw new Error('Failed to get brand strategy');
    }

    const brandData = await brandResponse.json();

    return {
      report_html: latestAnalysis.report_html,
      copy: latestAnalysis.copy,
      style: latestAnalysis.style,
      reference_point: brandData.reference_point,
      frame_shift: brandData.frame_shift,
      positioning: brandData.positioning
    };
  } catch (error) {
    console.error('Error fetching full report:', error);
    throw error;
  }
}

export default async function FullReportPage() {
  try {
    const reportData = await getFullReport();
    return <FullReportClient data={reportData} />;
  } catch (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            리포트를 불러오는데 실패했습니다
          </h1>
          <p className="text-gray-600">
            잠시 후 다시 시도해주세요.
          </p>
        </div>
      </div>
    );
  }
} 