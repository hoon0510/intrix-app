import Link from "next/link";
import Layout from "@/components/layout";

export default function AnalyzeIntroPage() {
  return (
    <Layout>
      <section className="max-w-3xl mx-auto py-24 px-6 text-center">
        <h1 className="text-4xl font-bold mb-6">Intrix 분석을 시작합니다</h1>
        <p className="text-gray-700 mb-6 leading-relaxed">
          Intrix는 단순한 텍스트 분석기가 아닙니다.<br />
          고객의 감정 흐름과 무의식적 욕구를 파악하고,<br />
          전환 가능한 전략 구조를 자동 설계하는 인사이트 플랫폼입니다.
        </p>
        <p className="text-sm text-gray-500 mb-10">
          분석 과정은 총 5단계로 구성되며, 입력하신 리뷰/피드백 데이터를 기반으로 전략과 콘텐츠 실행안까지 도출됩니다.
        </p>
        <Link
          href="/analyze/input"
          className="inline-block bg-black text-white px-6 py-3 rounded-lg font-medium hover:bg-gray-800 transition"
        >
          분석 시작하기 →
        </Link>
      </section>
    </Layout>
  );
} 