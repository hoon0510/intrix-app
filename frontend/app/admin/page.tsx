"use client";

import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2 } from "lucide-react";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";

interface User {
  email: string;
  credit: number;
  id: string;
}

export default function AdminPage() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [users, setUsers] = useState<User[]>([]);
  const [editing, setEditing] = useState<Record<string, number>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [updating, setUpdating] = useState<Record<string, boolean>>({});

  useEffect(() => {
    if (status === "unauthenticated") {
      router.replace("/login");
    } else if (session?.user?.email !== process.env.NEXT_PUBLIC_ADMIN_EMAIL) {
      router.replace("/");
    }
  }, [status, session, router]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await fetch("/api/admin/users");
        if (!res.ok) throw new Error("Failed to fetch users");
        const data = await res.json();
        setUsers(data);
      } catch (error) {
        console.error("Error fetching users:", error);
        alert("사용자 목록을 불러오는데 실패했습니다.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchUsers();
  }, []);

  const handleChange = (id: string, value: string) => {
    setEditing((prev) => ({ ...prev, [id]: parseInt(value) || 0 }));
  };

  const applyUpdate = async (id: string) => {
    setUpdating((prev) => ({ ...prev, [id]: true }));
    try {
      const res = await fetch(`/api/admin/users/${id}/credit`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ credit: editing[id] }),
      });

      if (!res.ok) throw new Error("Failed to update credit");

      setUsers((prev) =>
        prev.map((u) =>
          u.id === id ? { ...u, credit: editing[id] } : u
        )
      );
      alert("크레딧이 업데이트되었습니다.");
    } catch (error) {
      console.error("Error updating credit:", error);
      alert("크레딧 업데이트에 실패했습니다.");
    } finally {
      setUpdating((prev) => ({ ...prev, [id]: false }));
    }
  };

  if (status === "loading" || isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  if (!session || session.user?.email !== process.env.NEXT_PUBLIC_ADMIN_EMAIL) {
    return null;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">관리자 페이지</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">사용자 관리</h2>
        <div className="space-y-4">
          {users.map((u) => (
            <div
              key={u.id}
              className="border rounded p-4 flex items-center justify-between bg-white dark:bg-neutral-800"
            >
              <div>
                <p className="font-medium">{u.email}</p>
                <p className="text-sm text-gray-500">현재 크레딧: {u.credit}</p>
              </div>
              <div className="flex items-center gap-2">
                <Input
                  type="number"
                  defaultValue={u.credit}
                  onChange={(e) => handleChange(u.id, e.target.value)}
                  className="w-24"
                  min="0"
                />
                <Button
                  size="sm"
                  onClick={() => applyUpdate(u.id)}
                  disabled={updating[u.id]}
                >
                  {updating[u.id] ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    "업데이트"
                  )}
                </Button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
} 