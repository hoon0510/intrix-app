import type { Metadata } from "next";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { notFound, redirect } from "next/navigation";

export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  return {
    title: `Intrix 전략 리포트 – ${params.id}`,
    description: "Intrix 분석 결과 리포트",
    openGraph: {
      title: `Intrix 전략 리포트`,
      description: "AI 분석 기반 브랜드 전략 결과",
      images: ["https://your-intrix-domain.com/og-default.png"],
    },
  };
}

export default async function ResultPage({ params }: { params: { id: string } }) {
  const session = await getServerSession(authOptions);

  if (!session) {
    return redirect("/login");
  }

  // 이후 기존 분석 결과 렌더링 로직 진행
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">분석 결과</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <p>분석 ID: {params.id}</p>
        {/* 기존 분석 결과 렌더링 코드 */}
      </div>
    </div>
  );
} 