"use client";

import { ExecutionResult } from "./ExecutionResult";

interface Props {
  analysisId: string;
  inputText: string;
  result?: any;
  className?: string;
}

export default function AnalysisResult({ 
  analysisId, 
  inputText,
  result,
  className = "" 
}: Props) {
  return (
    <div className={className}>
      {result ? (
        <div>
          <h4 className="font-semibold mb-2">분석 결과</h4>
          <pre className="bg-gray-50 p-4 rounded overflow-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      ) : (
        <ExecutionResult analysisId={analysisId} />
      )}
    </div>
  );
} 