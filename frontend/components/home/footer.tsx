import Link from "next/link";

const Footer = () => {
  return (
    <footer className="w-full border-t bg-white z-10">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* 회사 정보 */}
          <div>
            <h3 className="text-sm font-semibold mb-4">Intrix</h3>
            <p className="text-xs text-muted-foreground">
              감정 기반 전략 자동화 도구
            </p>
          </div>

          {/* 빠른 링크 */}
          <div>
            <h3 className="text-sm font-semibold mb-4">바로가기</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/about" className="text-xs text-muted-foreground hover:text-primary">
                  회사 소개
                </Link>
              </li>
              <li>
                <Link href="/pricing" className="text-xs text-muted-foreground hover:text-primary">
                  요금제
                </Link>
              </li>
              <li>
                <Link href="/guide" className="text-xs text-muted-foreground hover:text-primary">
                  이용 가이드
                </Link>
              </li>
            </ul>
          </div>

          {/* 연락처 */}
          <div>
            <h3 className="text-sm font-semibold mb-4">문의하기</h3>
            <p className="text-xs text-muted-foreground">
              contact@intrix.ai
            </p>
          </div>
        </div>

        {/* 법적 안내 */}
        <div className="mt-8 pt-8 border-t">
          <p className="text-xs text-muted-foreground text-center">
            © 2025 Intrix. All rights reserved.
          </p>
          <p className="text-xs text-muted-foreground text-center mt-2">
            전략 자동화 책임 안내: Intrix는 감정과 욕구 분석을 기반으로 전략을 자동 생성하며, 
            결과물에 대한 최종 판단과 윤리적 책임은 사용자에게 있습니다.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 