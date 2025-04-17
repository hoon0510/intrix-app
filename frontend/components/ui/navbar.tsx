"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { label: "홈", href: "/" },
  { label: "분석기", href: "/analyzer" },
  { label: "전략 리포트", href: "/strategy" },
  { label: "마이페이지", href: "/mypage" },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="w-full flex justify-between items-center px-6 py-4 shadow-md bg-white sticky top-0 z-50">
      <div className="text-xl font-bold text-gray-800">INTRIX</div>
      <div className="flex space-x-6">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`text-sm font-medium ${
              pathname === item.href
                ? "text-black border-b-2 border-black pb-1"
                : "text-gray-500 hover:text-black"
            }`}
          >
            {item.label}
          </Link>
        ))}
      </div>
    </nav>
  );
} 