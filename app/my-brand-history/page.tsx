import React from 'react';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import BrandHistoryClient from './BrandHistoryClient';

async function getBrandHistory() {
  const cookieStore = await cookies();
  const authToken = cookieStore.get('auth_token')?.value;
  
  if (!authToken) {
    redirect('/login');
  }

  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/user/brand-history`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authToken}`
      },
      cache: 'no-store'
    });

    if (!response.ok) {
      throw new Error('Failed to fetch brand history');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching brand history:', error);
    throw error;
  }
}

export default async function BrandHistoryPage() {
  try {
    const history = await getBrandHistory();
    return <BrandHistoryClient items={history} />;
  } catch (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-red-600 mb-4">
            오류가 발생했습니다
          </h1>
          <p className="text-gray-600">
            브랜드 전략 이력을 불러오는 중 문제가 발생했습니다. 다시 시도해주세요.
          </p>
        </div>
      </div>
    );
  }
} 