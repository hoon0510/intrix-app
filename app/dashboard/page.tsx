import React from 'react';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import DashboardClient from './DashboardClient';
import ShareButton from '../components/ShareButton';
import DeleteShareButton from '../components/DeleteShareButton';

async function getDashboardData() {
  const cookieStore = await cookies();
  const authToken = cookieStore.get('auth_token')?.value;

  if (!authToken) {
    redirect('/login');
  }

  try {
    // Get user info
    const userResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/user/me`, {
      headers: {
        'Authorization': `Bearer ${authToken}`
      }
    });

    if (!userResponse.ok) {
      throw new Error('Failed to get user info');
    }

    const userData = await userResponse.json();
    const userId = userData.id;

    // Get analysis history
    const historyResponse = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/user/${userId}/history`,
      {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      }
    );

    if (!historyResponse.ok) {
      throw new Error('Failed to get analysis history');
    }

    const historyData = await historyResponse.json();
    const recentAnalyses = historyData.data.slice(0, 3);

    return {
      user: {
        total_analyses: historyData.data.length,
        credits: userData.credits,
        last_analysis: historyData.data[0]?.created_at || null
      },
      recentAnalyses
    };
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
    throw error;
  }
}

export default async function DashboardPage() {
  try {
    const dashboardData = await getDashboardData();
    const latestAnalysis = dashboardData.recentAnalyses[0];
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-2xl font-bold text-gray-900">대시보드</h1>
            {latestAnalysis && (
              <div className="flex space-x-2">
                <ShareButton analysisId={latestAnalysis.id} />
                {latestAnalysis.share_uuid && (
                  <DeleteShareButton 
                    shareUuid={latestAnalysis.share_uuid} 
                    onDelete={() => {
                      // Refresh the page to update the UI
                      window.location.reload();
                    }} 
                  />
                )}
              </div>
            )}
          </div>
          <DashboardClient data={dashboardData} />
        </div>
        <ToastContainer position="bottom-right" />
      </div>
    );
  } catch (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            대시보드를 불러오는데 실패했습니다
          </h1>
          <p className="text-gray-600">
            잠시 후 다시 시도해주세요.
          </p>
        </div>
      </div>
    );
  }
} 