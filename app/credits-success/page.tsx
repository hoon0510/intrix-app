'use client';

import React, { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';

export default function CreditsSuccessPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [isLoading, setIsLoading] = useState(true);
  const [creditsAdded, setCreditsAdded] = useState(0);

  useEffect(() => {
    const sessionId = searchParams.get('session_id');
    if (!sessionId) {
      router.push('/buy-credits');
      return;
    }

    // Verify payment and get credits added
    verifyPayment(sessionId);
  }, [searchParams]);

  const verifyPayment = async (sessionId: string) => {
    try {
      const response = await fetch(`/api/payment/verify?session_id=${sessionId}`);
      const data = await response.json();
      
      if (data.success) {
        setCreditsAdded(data.credits);
        setIsLoading(false);
      } else {
        router.push('/buy-credits');
      }
    } catch (error) {
      console.error('Error verifying payment:', error);
      router.push('/buy-credits');
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Verifying your payment...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
        <div className="mb-6">
          <svg
            className="w-16 h-16 text-green-500 mx-auto"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>
        <h1 className="text-2xl font-bold text-gray-900 mb-4">
          Payment Successful!
        </h1>
        <p className="text-gray-600 mb-6">
          {creditsAdded} credits have been added to your account.
        </p>
        <div className="space-y-4">
          <Link
            href="/buy-credits"
            className="block w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Buy More Credits
          </Link>
          <Link
            href="/"
            className="block w-full bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Return to Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
} 