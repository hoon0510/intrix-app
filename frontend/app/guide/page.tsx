import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Guide - Intrix',
  description: 'Learn how to use Intrix to analyze emotions and generate marketing strategies with our step-by-step guide.',
}

export default function GuidePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl mb-8">
          Intrix 사용 가이드
        </h1>

        <div className="prose prose-lg max-w-none">
          <ol className="list-decimal list-inside space-y-8">
            <li className="text-gray-800">
              <strong className="text-gray-900">회원가입 및 로그인</strong>
              <p className="mt-2 text-gray-600">
                Google 계정으로 간편하게 로그인하세요. 모든 분석 기능은 로그인 후 이용 가능합니다.
              </p>
            </li>

            <li className="text-gray-800">
              <strong className="text-gray-900">분석할 텍스트 입력</strong>
              <p className="mt-2 text-gray-600">
                리뷰, 댓글, 키워드 등 분석하고자 하는 텍스트를 입력합니다. 최대 1000자까지 지원됩니다.
              </p>
            </li>

            <li className="text-gray-800">
              <strong className="text-gray-900">분석 탭 선택</strong>
              <p className="mt-2 text-gray-600">
                다층욕구 분석, 신규 유입 분석, 리텐션 분석 등 목적에 맞는 분석 탭을 선택하세요.
              </p>
            </li>

            <li className="text-gray-800">
              <strong className="text-gray-900">전략 결과 확인</strong>
              <p className="mt-2 text-gray-600">
                감정 흐름, 욕구 구조, 전략 방향, 카피라이팅 결과를 구조화된 보고서 형식으로 확인할 수 있습니다.
              </p>
            </li>

            <li className="text-gray-800">
              <strong className="text-gray-900">결과 저장 및 다운로드</strong>
              <p className="mt-2 text-gray-600">
                즐겨찾기 기능을 통해 원하는 결과를 저장하고 PDF로 다운로드할 수 있습니다.
              </p>
            </li>
          </ol>

          <div className="mt-12 p-6 bg-blue-50 rounded-lg">
            <p className="text-lg text-gray-800">
              Intrix는 단순한 감정 분석 도구가 아닙니다. 감정 구조를 기반으로 전략을 자동 생성하는 마케팅 전략가입니다.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
} 