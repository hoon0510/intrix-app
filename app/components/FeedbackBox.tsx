'use client';

import React, { useState } from 'react';
import { toast } from 'react-toastify';

interface FeedbackBoxProps {
  analysisId: string;
  className?: string;
}

export function FeedbackBox({ analysisId, className = '' }: FeedbackBoxProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleFeedback = async (isHelpful: boolean) => {
    if (isSubmitting) return;
    
    setIsSubmitting(true);
    
    try {
      const response = await fetch('/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          analysis_id: analysisId,
          is_helpful: isHelpful,
        }),
      });

      if (!response.ok) {
        throw new Error('피드백 전송에 실패했습니다');
      }

      toast.success('피드백을 보내주셔서 감사합니다!', {
        autoClose: 2000,
        className: 'bg-green-50 border-l-4 border-green-400 text-green-700',
      });
    } catch (error) {
      console.error('Feedback submission failed:', error);
      toast.error('피드백 전송에 실패했습니다', {
        autoClose: 2000,
        className: 'bg-red-50 border-l-4 border-red-400 text-red-700',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <span className="text-sm text-gray-500">이 전략이 도움이 되었나요?</span>
      <div className="flex items-center gap-2">
        <button
          onClick={() => handleFeedback(true)}
          disabled={isSubmitting}
          className="p-1 rounded-full hover:bg-gray-100 transition-colors disabled:opacity-50"
          title="도움됨"
        >
          👍
        </button>
        <button
          onClick={() => handleFeedback(false)}
          disabled={isSubmitting}
          className="p-1 rounded-full hover:bg-gray-100 transition-colors disabled:opacity-50"
          title="도움 안됨"
        >
          👎
        </button>
      </div>
    </div>
  );
} 