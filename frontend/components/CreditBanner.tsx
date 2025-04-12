import React from 'react';

interface CreditBannerProps {
  finalCredit: number;
  freeTrial: boolean;
}

const CreditBanner: React.FC<CreditBannerProps> = ({ finalCredit, freeTrial }) => {
  if (freeTrial && finalCredit === 0) {
    return (
      <div className="w-full bg-blue-50 border-l-4 border-blue-500 p-4 mb-4">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-blue-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <p className="text-sm text-blue-700">
              이번 분석은 무료 체험으로 제공되었습니다
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full bg-gray-50 border-l-4 border-gray-500 p-4 mb-4">
      <div className="flex items-center">
        <div className="flex-shrink-0">
          <svg className="h-5 w-5 text-gray-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
        </div>
        <div className="ml-3">
          <p className="text-sm text-gray-700">
            총 {finalCredit} 크레딧이 사용되었습니다
          </p>
        </div>
      </div>
    </div>
  );
};

export default CreditBanner; 