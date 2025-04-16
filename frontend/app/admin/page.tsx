"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

interface Stats {
  total_requests: number;
  total_credits: number;
  recent_activity: Array<{
    date: string;
    count: number;
  }>;
}

interface ApiResponse {
  status: string;
  data?: Stats;
  error?: string;
}

export default function AdminPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const fetchStats = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        const response = await fetch("/api/admin/stats");
        const result: ApiResponse = await response.json();
        
        if (!response.ok || result.status !== "ok") {
          throw new Error(result.error || "통계 데이터를 불러오는데 실패했습니다.");
        }
        
        if (!result.data) {
          throw new Error("데이터가 없습니다.");
        }
        
        setStats(result.data);
      } catch (err) {
        console.error("Admin stats fetch error:", err);
        setError(err instanceof Error ? err.message : "알 수 없는 오류가 발생했습니다.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (isLoading) {
    return (
      <div className="max-w-3xl mx-auto p-6">
        <div className="flex items-center space-x-2">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500" />
          <p className="text-sm text-gray-400">데이터를 불러오는 중...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-3xl mx-auto p-6">
        <div className="p-4 border border-red-200 rounded-lg bg-red-50">
          <p className="text-red-500 font-medium">오류 발생</p>
          <p className="text-sm text-red-600 mt-1">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="mt-2 text-sm text-red-600 hover:text-red-700"
          >
            다시 시도
          </button>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="max-w-3xl mx-auto p-6">
        <div className="p-4 border border-gray-200 rounded-lg bg-gray-50">
          <p className="text-gray-500">데이터가 없습니다.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-xl font-bold">Admin 대시보드</h1>
        <button
          onClick={() => router.push("/")}
          className="text-sm text-gray-500 hover:text-gray-700"
        >
          메인으로 돌아가기
        </button>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="p-4 border rounded-xl bg-white shadow-sm">
          <p className="text-gray-500 text-sm">전체 요청 수</p>
          <p className="text-2xl font-bold mt-2">{stats.total_requests.toLocaleString()}</p>
        </div>
        <div className="p-4 border rounded-xl bg-white shadow-sm">
          <p className="text-gray-500 text-sm">총 크레딧 사용</p>
          <p className="text-2xl font-bold mt-2">{stats.total_credits.toLocaleString()}</p>
        </div>
      </div>

      <div className="p-4 border rounded-xl bg-white shadow-sm">
        <h2 className="text-sm font-semibold mb-4">최근 7일 요청 수</h2>
        <div className="space-y-3">
          {stats.recent_activity.length === 0 ? (
            <p className="text-sm text-gray-500">최근 요청 데이터가 없습니다.</p>
          ) : (
            stats.recent_activity.map((day) => (
              <div key={day.date} className="flex items-center">
                <span className="w-32 text-gray-600">{day.date}</span>
                <div className="flex-1">
                  <div className="h-4 bg-blue-100 rounded-full">
                    <div
                      className="h-full bg-blue-500 rounded-full"
                      style={{
                        width: `${(day.count / Math.max(...stats.recent_activity.map(d => d.count))) * 100}%`
                      }}
                    />
                  </div>
                </div>
                <span className="w-16 text-right text-sm font-medium">
                  {day.count.toLocaleString()}회
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
} 