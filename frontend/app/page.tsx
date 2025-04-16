import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-white text-gray-900 px-6 py-20 flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-4 text-center">Intrix</h1>
      <p className="text-lg mb-8 text-center max-w-xl">
        감정과 욕구 기반 전략 자동화 시스템.
        Intrix는 고객의 무의식, 니즈, 전환 흐름을 정밀하게 해석하여
        전략과 카피를 자동 설계합니다.
      </p>
      <div className="flex flex-col sm:flex-row gap-4">
        <Link href="/analyze" className="px-6 py-3 bg-black text-white rounded-xl text-center font-semibold">
          전략 분석 시작하기
        </Link>
        <Link href="/login" className="px-6 py-3 border border-black text-black rounded-xl text-center font-semibold">
          로그인
        </Link>
      </div>
    </main>
  );
} 