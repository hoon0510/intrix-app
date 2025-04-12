import React from 'react';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import BrandResultClient from './ABResultClient';
import ShareButton from '../components/ShareButton';

async function getBrandStrategy() {
  const cookieStore = await cookies();
  const authToken = cookieStore.get('auth_token')?.value;
  
  if (!authToken) {
    redirect('/login');
  }

  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/brand-strategy`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`
      },
      body: JSON.stringify({
        strategy: {
          // TODO: Replace with actual strategy data
          core_message: "테스트 메시지",
          differentiation: "테스트 차별화",
          target: "테스트 타겟"
        }
      }),
      cache: 'no-store'
    });

    if (!response.ok) {
      throw new Error('Failed to fetch brand strategy');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching brand strategy:', error);
    throw error;
  }
}

export default async function BrandResultPage() {
  try {
    const result = await getBrandStrategy();
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-2xl font-bold text-gray-900">브랜드 전략 결과</h1>
            {result && (
              <ShareButton analysisId={result.id} />
            )}
          </div>
          <BrandResultClient result={result} />
        </div>
      </div>
    );
  } catch (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-red-600 mb-4">
            오류가 발생했습니다
          </h1>
          <p className="text-gray-600">
            브랜드 전략 결과를 불러오는 중 문제가 발생했습니다. 다시 시도해주세요.
          </p>
        </div>
      </div>
    );
  }
} 