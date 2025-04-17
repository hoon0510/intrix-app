"use client";

import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Star } from "lucide-react";

interface AnalysisRecord {
  job_id: string;
  item_name: string;
  created_at: string;
  favorite: boolean;
}

interface UserInfo {
  email: string;
  credit: number;
}

export default function MyPage() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [records, setRecords] = useState<AnalysisRecord[]>([]);

  useEffect(() => {
    if (status === "unauthenticated") {
      router.replace("/login");
    }
  }, [status, router]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch("/api/user/me");
        if (!res.ok) throw new Error("Failed to fetch user data");
        const data = await res.json();
        setRecords(data.history);
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    };
    fetchData();
  }, []);

  const toggleFavorite = async (job_id: string) => {
    try {
      const res = await fetch(`/api/analysis/${job_id}/favorite`, {
        method: "PATCH",
      });
      if (!res.ok) throw new Error("Failed to toggle favorite");
      setRecords((prev) =>
        prev.map((r) =>
          r.job_id === job_id ? { ...r, favorite: !r.favorite } : r
        )
      );
    } catch (error) {
      console.error("Error toggling favorite:", error);
    }
  };

  if (status === "loading") {
    return <p className="text-center py-10">로그인 상태 확인 중...</p>;
  }

  if (!session) {
    return null;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">마이페이지</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <div className="mb-4">
          <h2 className="text-lg font-semibold mb-2">계정 정보</h2>
          <p>이메일: {session.user?.email}</p>
        </div>
        <div>
          <h2 className="text-lg font-semibold mb-2">사용 내역</h2>
          <p>남은 크레딧: {session.user?.credit || 0}</p>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>분석 이력</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {records.length === 0 ? (
              <p className="text-center text-gray-500">아직 분석 기록이 없습니다.</p>
            ) : (
              records.map((r) => (
                <div
                  key={r.job_id}
                  className="flex justify-between items-center p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-neutral-800 transition-colors"
                >
                  <div>
                    <div className="font-medium">{r.item_name}</div>
                    <div className="text-sm text-gray-500">
                      {new Date(r.created_at).toLocaleString()}
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <a
                      href={`/result/${r.job_id}`}
                      className="text-blue-600 hover:underline text-sm"
                    >
                      보기
                    </a>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => toggleFavorite(r.job_id)}
                      className="text-yellow-500 hover:text-yellow-600"
                    >
                      <Star
                        className={`h-4 w-4 mr-2 ${
                          r.favorite ? "fill-current" : ""
                        }`}
                      />
                      {r.favorite ? "즐겨찾기 해제" : "즐겨찾기 등록"}
                    </Button>
                  </div>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
} 