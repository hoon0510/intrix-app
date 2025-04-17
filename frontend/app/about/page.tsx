import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'About - Intrix',
  description: 'Discover how Intrix transforms emotional insights into powerful marketing strategies through AI-powered analysis.',
}

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl mb-12">
          Intrix란?
        </h1>

        <div className="prose prose-lg max-w-none space-y-12">
          <section className="bg-white p-8 rounded-xl shadow-sm">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              📌 전략 자동화, 그 너머
            </h2>
            <p className="text-gray-600">
              Intrix는 단순한 AI 분석 툴이 아닙니다. 감정과 욕구를 읽고, 전략을 설계하며, 행동을 유도하는 실전형 마케팅 자동화 시스템입니다.
              단어 하나에도 전환의 흐름이 설계되고, 모든 전략은 정량화된 감정 데이터에서 출발합니다.
            </p>
          </section>

          <section className="bg-white p-8 rounded-xl shadow-sm">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              🚀 Intrix의 핵심 기능
            </h2>
            <ul className="list-disc list-inside text-gray-600 space-y-2">
              <li>다층 감정 및 욕구 분석</li>
              <li>자동 전략 기획안 및 브랜딩 생성</li>
              <li>자극형 카피라이팅 출력</li>
              <li>PDF 보고서 다운로드 및 즐겨찾기</li>
              <li>Claude + GPT 병렬 구조 기반 고정된 전략 설계 흐름</li>
            </ul>
          </section>

          <section className="bg-white p-8 rounded-xl shadow-sm">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              ⚙️ 무엇이 다른가?
            </h2>
            <p className="text-gray-600">
              대부분의 AI 도구가 '요약'에 머무르는 반면, Intrix는 '전략'을 설계합니다.  
              우리는 데이터 기반 마케터의 언어를 알고, 프레임 전환과 감정 유도 흐름을 시스템화합니다.
              그리고 그 결과는 누구도 수정할 수 없습니다. 카피를 제외하고는.
            </p>
          </section>
        </div>
      </div>
    </div>
  )
} 