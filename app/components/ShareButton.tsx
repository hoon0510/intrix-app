import React from 'react';
import { toast } from 'react-toastify';

interface ShareButtonProps {
  analysisId: string;
}

export default function ShareButton({ analysisId }: ShareButtonProps) {
  const handleShare = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/share-link`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          analysis_id: analysisId,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate share link');
      }

      const data = await response.json();
      navigator.clipboard.writeText(data.share_url);
      toast.success('공유 링크가 복사되었습니다');
    } catch (error) {
      console.error('Error generating share link:', error);
      toast.error('공유 링크 생성에 실패했습니다');
    }
  };

  return (
    <button
      onClick={handleShare}
      className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
    >
      공유하기
    </button>
  );
} 