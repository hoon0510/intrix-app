"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import AuthGuard from "@/components/auth/AuthGuard";

interface User {
  id: string;
  email: string;
  name: string | null;
  role: string;
  credit: number;
}

export default function Page() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [creditAmount, setCreditAmount] = useState("");

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch("/api/admin/users");
      if (!response.ok) throw new Error("Failed to fetch users");
      const data = await response.json();
      setUsers(data);
    } catch (err) {
      setError("사용자 목록을 불러오는데 실패했습니다.");
    } finally {
      setLoading(false);
    }
  };

  const handleAddCredit = async (userId: string) => {
    if (!creditAmount) return;
    
    try {
      const response = await fetch(`/api/admin/users/${userId}/credit`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ amount: parseInt(creditAmount) }),
      });

      if (!response.ok) throw new Error("Failed to add credit");
      
      await fetchUsers();
      setCreditAmount("");
    } catch (err) {
      setError("크레딧 추가에 실패했습니다.");
    }
  };

  if (loading) return <div>로딩 중...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">관리자 페이지</h1>
        
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>사용자 관리</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {users.map((user) => (
                <div key={user.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <p className="font-medium">{user.email}</p>
                    <p className="text-sm text-gray-500">크레딧: {user.credit}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Input
                      type="number"
                      value={creditAmount}
                      onChange={(e) => setCreditAmount(e.target.value)}
                      placeholder="크레딧 금액"
                      className="w-32"
                    />
                    <Button onClick={() => handleAddCredit(user.id)}>
                      크레딧 추가
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </AuthGuard>
  );
} 