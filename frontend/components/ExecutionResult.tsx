"use client";

import { useEffect, useState } from "react";

interface ExecutionData {
  id: string;
  hook: string;
  flow: string;
  cta: string;
  created_at: string;
}

interface ExecutionResultProps {
  analysisId: string;
  className?: string;
}

export function ExecutionResult({ analysisId, className = "" }: ExecutionResultProps) {
  const [data, setData] = useState<ExecutionData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [generating, setGenerating] = useState(false);

  const fetchData = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await fetch(`/api/execution/${analysisId}`);
      if (!response.ok) {
        throw new Error("실행 전략을 불러오는데 실패했습니다.");
      }
      const data = await response.json();
      setData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "알 수 없는 오류가 발생했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateExecution = async () => {
    try {
      setGenerating(true);
      setError(null);
      const response = await fetch(`/api/execution/${analysisId}`, {
        method: "POST",
      });
      if (!response.ok) {
        throw new Error("실행 전략 생성에 실패했습니다.");
      }
      const data = await response.json();
      setData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "알 수 없는 오류가 발생했습니다.");
    } finally {
      setGenerating(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [analysisId]);

  if (error) {
    return (
      <div className={`p-4 bg-red-50 rounded-lg ${className}`}>
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
    );
  }

  if (isLoading) {
    return (
      <div className={`flex items-center justify-center p-4 ${className}`}>
        <svg className="animate-spin h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
        <span className="ml-2 text-sm text-gray-500">실행 전략을 불러오는 중...</span>
      </div>
    );
  }

  if (!data) {
    return (
      <div className={`p-4 ${className}`}>
        <p className="text-sm text-gray-400 mb-3">실행 전략이 아직 없습니다.</p>
        <button
          onClick={handleGenerateExecution}
          disabled={generating}
          className="text-sm text-blue-600 hover:text-blue-800 disabled:text-gray-400 disabled:cursor-not-allowed"
        >
          {generating ? "생성 중..." : "실행 전략 생성"}
        </button>
      </div>
    );
  }

  return (
    <div className={`space-y-4 bg-white p-6 rounded-xl border shadow-sm ${className}`}>
      <div className="space-y-2">
        <h3 className="text-lg font-semibold text-gray-900">콘텐츠 실행 전략</h3>
        <p className="text-sm text-gray-500">
          {new Date(data.created_at).toLocaleString()}에 생성됨
        </p>
      </div>
      
      <div className="space-y-4">
        <div className="space-y-1">
          <h4 className="font-medium text-gray-700">HOOK</h4>
          <p className="text-gray-600 whitespace-pre-line">{data.hook}</p>
        </div>
        
        <div className="space-y-1">
          <h4 className="font-medium text-gray-700">FLOW</h4>
          <p className="text-gray-600 whitespace-pre-line">{data.flow}</p>
        </div>
        
        <div className="space-y-1">
          <h4 className="font-medium text-gray-700">CTA</h4>
          <p className="text-gray-600 whitespace-pre-line">{data.cta}</p>
        </div>
      </div>
    </div>
  );
}