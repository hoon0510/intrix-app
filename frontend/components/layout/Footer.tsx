import Link from "next/link";

const Footer = () => {
  return (
    <footer className="w-full border-t py-6">
      <div className="max-w-4xl mx-auto px-4">
        <p className="text-sm text-center text-gray-500">
          © 2025 Intrix. 모든 전략 결과는 사용자 책임 하에 활용됩니다.
        </p>
        <p className="mt-2 text-xs text-center text-gray-500">
          "Intrix는 전략 자동화를 위한 도구이며, 윤리적 판단과 실행 책임은 사용자에게 있습니다."
        </p>
        
        <div className="mt-8 pt-6 border-t">
          <p className="text-xs text-center text-gray-500">
            전략 자동화 책임 안내<br />
            Intrix는 고객의 감정과 욕구 분석을 기반으로 전략과 카피를 자동 생성합니다. 
            저희 시스템은 데이터 기반 인사이트를 제공하지만, 그 결과에 대한 가치 판단은 하지 않습니다. 
            제안된 전략의 윤리적 적합성과 실행 여부는 전적으로 이용자의 판단에 달려 있습니다. 
            Intrix는 전략 자동화를 위한 도구로서, 최종 결정과 그에 따른 윤리적 책임은 사용자에게 있음을 안내드립니다.
          </p>
          <div className="mt-4 text-center">
            <Link 
              href="/terms" 
              className="text-xs text-blue-600 hover:text-blue-800 underline"
            >
              이용약관 보기
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 