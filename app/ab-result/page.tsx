import { getServerSession } from "next-auth";
import { redirect } from "next/navigation";
import ABResultClient from "./ABResultClient";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import ShareButton from "@/app/components/ShareButton";

async function getABTestResults() {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/ab-test`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        input_text: "테스트 텍스트",
        channels: ["twitter", "linkedin"],
        variant_count: 2
      }),
      cache: 'no-store'
    });

    if (!response.ok) {
      throw new Error('Failed to fetch A/B test results');
    }

    const data = await response.json();
    return {
      variantA: {
        id: data.variants[0].id,
        copy: data.variants[0].copy,
        style: data.variants[0].style,
        report_html: data.variants[0].report_html
      },
      variantB: {
        id: data.variants[1].id,
        copy: data.variants[1].copy,
        style: data.variants[1].style,
        report_html: data.variants[1].report_html
      }
    };
  } catch (error) {
    console.error('Error fetching A/B test results:', error);
    throw error;
  }
}

export default async function ABResultPage() {
  const session = await getServerSession(authOptions);
  
  if (!session) {
    redirect("/login");
  }

  try {
    const results = await getABTestResults();
    return <ABResultClient variantA={results.variantA} variantB={results.variantB} />;
  } catch (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-red-600 mb-4">
            오류가 발생했습니다
          </h1>
          <p className="text-gray-600">
            A/B 테스트 결과를 불러오는 중 문제가 발생했습니다. 다시 시도해주세요.
          </p>
        </div>
      </div>
    );
  }
} 