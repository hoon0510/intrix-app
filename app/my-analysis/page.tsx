'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import ShareButton from '../components/ShareButton';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import DeleteShareButton from '../components/DeleteShareButton';

interface AnalysisResult {
  id: string;
  date: string;
  channels: string[];
  copy: string;
  strategySummary: string;
  reportHtml: string;
}

// Mock data
const mockAnalysisResults: AnalysisResult[] = [
  {
    id: '1',
    date: '2024-04-12',
    channels: ['Twitter', 'LinkedIn', 'Reddit'],
    copy: 'Transform your marketing with AI-powered insights that drive real results.',
    strategySummary: 'Focus on social proof and data-driven decision making',
    reportHtml: '<div>Report content...</div>',
  },
  {
    id: '2',
    date: '2024-04-11',
    channels: ['Facebook', 'Instagram'],
    copy: 'Unlock the power of your data with our advanced analytics platform.',
    strategySummary: 'Emphasize ease of use and integration capabilities',
    reportHtml: '<div>Report content...</div>',
  },
];

async function getAnalysisHistory() {
  const token = cookies().get('token')?.value;
  if (!token) {
    redirect('/login');
  }

  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/user/${token}/history`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch analysis history');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching analysis history:', error);
    throw error;
  }
}

export default async function MyAnalysisPage() {
  const history = await getAnalysisHistory();

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">내 분석 결과</h1>
        
        <div className="grid grid-cols-1 gap-6">
          {history.data.map((item: any) => (
            <div key={item.id} className="bg-white shadow rounded-lg p-6">
              <div className="flex justify-between items-start">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">{item.input_text}</h2>
                  <p className="text-sm text-gray-500 mt-1">
                    {new Date(item.timestamp).toLocaleString()}
                  </p>
                </div>
                <div className="flex space-x-2">
                  <ShareButton analysisId={item.id} />
                  {item.share_uuid && (
                    <DeleteShareButton 
                      shareUuid={item.share_uuid} 
                      onDelete={() => {
                        // Refresh the page to update the UI
                        window.location.reload();
                      }} 
                    />
                  )}
                </div>
              </div>
              
              <div className="mt-4">
                <div className="prose max-w-none">
                  <div dangerouslySetInnerHTML={{ __html: item.report_html }} />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
      <ToastContainer position="bottom-right" />
    </div>
  );
} 