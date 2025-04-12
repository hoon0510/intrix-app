import React from 'react';
import { notFound } from 'next/navigation';
import ShareClient from './ShareClient';
import { Metadata } from 'next';

async function getSharedAnalysis(uuid: string) {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/share/${uuid}`, {
      cache: 'no-store'
    });
    
    if (response.status === 404) {
      const errorData = await response.json();
      if (errorData.detail === "공유 링크가 만료되었습니다. 새 링크를 생성해 주세요.") {
        throw new Error('EXPIRED_LINK');
      }
      notFound();
    }
    
    if (!response.ok) {
      throw new Error('Failed to fetch analysis');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching shared analysis:', error);
    throw error;
  }
}

export async function generateMetadata({ params }: { params: { uuid: string } }): Promise<Metadata> {
  try {
    const data = await getSharedAnalysis(params.uuid);
    
    const title = data.positioning || 'Intrix 전략 리포트 공유';
    const description = data.copy || 'Intrix를 통해 생성된 마케팅 전략 리포트입니다.';
    const url = `${process.env.NEXT_PUBLIC_BASE_URL}/share/${params.uuid}`;
    
    return {
      title,
      description,
      openGraph: {
        title: data.positioning,
        description: data.copy,
        url,
        type: 'website',
      },
      twitter: {
        card: 'summary',
        title: data.positioning,
        description: data.copy,
      },
    };
  } catch (error) {
    return {
      title: 'Intrix 전략 리포트 공유',
      description: 'Intrix를 통해 생성된 마케팅 전략 리포트입니다.',
    };
  }
}

export default async function SharePage({ params }: { params: { uuid: string } }) {
  try {
    const data = await getSharedAnalysis(params.uuid);
    return <ShareClient data={data} />;
  } catch (error) {
    if (error instanceof Error && error.message === 'EXPIRED_LINK') {
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
          <div className="max-w-md w-full">
            <div className="bg-gray-100 rounded-lg p-6 text-center">
              <h1 className="text-2xl font-bold text-gray-900 mb-4">공유 링크가 만료되었습니다</h1>
              <p className="text-gray-600 mb-6">
                공유 링크는 24시간 동안만 유효합니다. 새로운 링크를 요청해주세요.
              </p>
              <a
                href="/"
                className="inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                홈으로 돌아가기
              </a>
            </div>
          </div>
        </div>
      );
    }
    
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">오류가 발생했습니다</h1>
          <p className="text-gray-600">분석 결과를 불러오는 중 문제가 발생했습니다.</p>
        </div>
      </div>
    );
  }
} 