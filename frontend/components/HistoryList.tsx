"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { HistoryItem } from "../types/history";
import AnalysisResult from "./AnalysisResult";

interface HistoryListProps {
  items: HistoryItem[];
  onItemClick?: (item: HistoryItem) => void;
}

export default function HistoryList({ items, onItemClick }: HistoryListProps) {
  const router = useRouter();
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());

  const toggleExpand = (id: string) => {
    setExpandedItems((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };

  return (
    <div className="space-y-4">
      {items.map((item) => (
        <div
          key={item.id}
          className="bg-white rounded-lg shadow p-4 cursor-pointer hover:shadow-md transition-shadow"
          onClick={() => onItemClick?.(item)}
        >
          <div className="flex justify-between items-start">
            <div>
              <h3 className="text-lg font-semibold">{item.input_text}</h3>
              <p className="text-sm text-gray-500">
                {new Date(item.created_at).toLocaleDateString()}
              </p>
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation();
                toggleExpand(item.id);
              }}
              className="flex items-center space-x-2 text-blue-500 hover:text-blue-700"
            >
              <span>분석 결과 보기</span>
              {expandedItems.has(item.id) ? (
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="m18 15-6-6-6 6"/>
                </svg>
              ) : (
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="m6 9 6 6 6-6"/>
                </svg>
              )}
            </button>
          </div>

          {expandedItems.has(item.id) && (
            <div className="mt-4">
              <AnalysisResult 
                analysisId={item.id}
                inputText={item.input_text}
                result={JSON.parse(item.result_json)}
              />
            </div>
          )}
        </div>
      ))}
    </div>
  );
} 