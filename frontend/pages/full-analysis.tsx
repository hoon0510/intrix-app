import React, { useState } from 'react';
import { withAuth } from '../utils/auth';
import CreditBanner from '../components/CreditBanner';

interface AnalysisResult {
  final_credit: number;
  from_cache: boolean;
  free_trial: boolean;
  copy: string;
  report_html: string;
}

const FullAnalysisPage: React.FC = () => {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalysis = async (text: string, channels: string[]) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/full_analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
        },
        body: JSON.stringify({
          input_text: text,
          channels: channels
        })
      });

      if (!response.ok) {
        if (response.status === 403) {
          // Handle authentication error
          setError('인증이 필요합니다. 다시 로그인해주세요.');
          return;
        }
        throw new Error('분석 중 오류가 발생했습니다.');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {result && (
        <CreditBanner 
          finalCredit={result.final_credit}
          freeTrial={result.free_trial}
        />
      )}
      
      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Add your analysis form and result display components here */}
    </div>
  );
};

export default withAuth(FullAnalysisPage); 