import Layout from "@/components/layout";

export default function AboutPage() {
  return (
    <Layout>
      <section className="max-w-4xl mx-auto py-20 px-6">
        <h1 className="text-3xl font-bold mb-4">INTRIX에 대해</h1>
        <p className="text-gray-700 mb-6">
          INTRIX는 인간의 감정 흐름과 무의식적 욕구를 AI가 분석하고,
          전략과 카피를 자동으로 생성하는 전략 자동화 시스템입니다.
          기존 마케팅의 주관성과 감에 의존하던 방식을 벗어나,
          데이터 기반의 정교한 전략 설계를 가능하게 합니다.
        </p>

        <h2 className="text-xl font-semibold mb-2">시스템 구조</h2>
        <ul className="list-disc ml-6 mb-6 text-gray-700">
          <li>① Claude 기반 감정·욕구 분석</li>
          <li>② GPT 기반 전략 설계 및 카피라이팅</li>
          <li>③ 포맷팅 및 사용자 맞춤 리포트 생성</li>
          <li>④ 실행 전략 및 채널별 콘텐츠 설계</li>
        </ul>

        <h2 className="text-xl font-semibold mb-2">윤리적 책임 고지</h2>
        <p className="text-gray-600 text-sm bg-gray-100 p-4 rounded-md">
          전략 자동화 책임 안내<br />
          Intrix는 고객의 감정과 욕구 분석을 기반으로 전략과 카피를 자동 생성합니다. 저희 시스템은 데이터 기반 인사이트를 제공하지만, 그 결과에 대한 가치 판단은 하지 않습니다. 제안된 전략의 윤리적 적합성과 실행 여부는 전적으로 이용자의 판단에 달려 있습니다. Intrix는 전략 자동화를 위한 도구로서, 최종 결정과 그에 따른 윤리적 책임은 사용자에게 있음을 안내드립니다.
        </p>
      </section>
    </Layout>
  );
} 