export default function HowItWorks() {
  const steps = [
    {
      title: "텍스트 입력",
      description: "분석하고 싶은 텍스트를 입력하세요. 리뷰, 피드백, 소셜 미디어 게시물 등 어떤 텍스트든 가능합니다.",
      icon: "📝"
    },
    {
      title: "AI 분석",
      description: "AI가 텍스트를 분석하여 감정, 욕구, 키워드를 추출합니다.",
      icon: "🤖"
    },
    {
      title: "전략 생성",
      description: "분석 결과를 바탕으로 최적의 마케팅 전략을 생성합니다.",
      icon: "🎯"
    },
    {
      title: "결과 확인",
      description: "생성된 전략과 실행 가이드를 확인하고 바로 적용해보세요.",
      icon: "📊"
    }
  ];

  return (
    <section id="how-it-works" className="w-full py-20 bg-gray-50">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">작동 방식</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <div key={index} className="relative">
              <div className="p-6 rounded-xl bg-white shadow-sm hover:shadow-md transition">
                <div className="text-4xl mb-4">{step.icon}</div>
                <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
                <p className="text-gray-600">{step.description}</p>
              </div>
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-1/2 right-0 transform -translate-y-1/2 translate-x-1/2">
                  <svg className="w-6 h-6 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
} 