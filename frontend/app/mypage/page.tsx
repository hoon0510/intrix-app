"use client";

import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import FavoriteList from "../../components/FavoriteList";

export default function MyPage() {
  const { data: session, status } = useSession();
  const router = useRouter();

  if (status === "loading") {
    return <div>Loading...</div>;
  }

  if (!session) {
    router.push("/login");
    return null;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">내 즐겨찾기</h1>
        <FavoriteList />
      </div>
    </div>
  );
} 