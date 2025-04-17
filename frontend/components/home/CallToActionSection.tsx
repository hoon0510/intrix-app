import Link from "next/link";

export default function CallToActionSection() {
  return (
    <section className="bg-neutral-950 py-16 text-center text-white">
      <div className="max-w-4xl mx-auto px-4">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          지금 바로 당신의 전략을 자동화하세요
        </h2>
        <p className="text-lg text-neutral-300 mb-6">
          Intrix는 감정과 욕구를 정밀하게 분석하여 마케팅 전략을 자동 생성하는 도구입니다.
          더 이상 감에 의존하지 마세요.
        </p>
        <Link 
          href="/analyze" 
          className="inline-block bg-white text-black px-6 py-3 rounded-full font-semibold hover:bg-neutral-200 transition"
        >
          전략 분석 시작하기
        </Link>
      </div>
    </section>
  );
} 