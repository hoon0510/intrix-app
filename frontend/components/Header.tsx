import Link from "next/link";

const Header = () => {
  return (
    <header className="fixed top-0 w-full z-50 border-b bg-white/80 backdrop-blur-md text-sm">
      <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
        <div className="font-bold">INTRIX</div>
        <nav className="space-x-4 text-gray-700">
          <Link href="/home" className="hover:underline">홈</Link>
          <Link href="/analyzer" className="hover:underline">분석</Link>
          <Link href="/mypage" className="hover:underline">마이페이지</Link>
        </nav>
      </div>
    </header>
  );
};

export default Header; 