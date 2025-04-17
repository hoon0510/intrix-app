export default function Credibility() {
  return (
    <section className="bg-white py-20">
      <div className="max-w-4xl mx-auto text-center px-4">
        <h2 className="text-3xl font-bold mb-6">자동화지만, 허술하지 않습니다</h2>
        <p className="text-gray-600 text-lg">
          Intrix는 단순 요약이 아닙니다. 감정 흐름 → 욕구 분해 → 전략 설계 → 실행 설계까지
          인간의 사고 흐름을 정밀하게 반영해 설계됩니다.
        </p>
        <div className="mt-10 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-gray-100 p-6 rounded-xl shadow-sm">
            <h3 className="font-semibold text-xl mb-2">40개 욕구 체계</h3>
            <p className="text-sm text-gray-600">상위/하위 욕구로 세분화된 구조 기반 분석</p>
          </div>
          <div className="bg-gray-100 p-6 rounded-xl shadow-sm">
            <h3 className="font-semibold text-xl mb-2">다단계 프롬프트 설계</h3>
            <p className="text-sm text-gray-600">모델별 역할 분리와 단계별 응답 흐름</p>
          </div>
          <div className="bg-gray-100 p-6 rounded-xl shadow-sm">
            <h3 className="font-semibold text-xl mb-2">비즈니스 실전 최적화</h3>
            <p className="text-sm text-gray-600">보고서 포맷, 실행 가능성 중심 구조 설계</p>
          </div>
        </div>
      </div>
    </section>
  );
} 