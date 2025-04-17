"use client";

import Link from "next/link";
import { useSession, signIn, signOut } from "next-auth/react";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "./theme-toggle";

const Header = () => {
  const { data: session, status } = useSession();

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 hidden md:flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <span className="hidden font-bold sm:inline-block">
              Intrix
            </span>
          </Link>
          <nav className="flex items-center space-x-6 text-sm font-medium">
            <Link
              href="/analyzer"
              className="transition-colors hover:text-foreground/80 text-foreground/60"
            >
              분석하기
            </Link>
            <Link
              href="/about"
              className="transition-colors hover:text-foreground/80 text-foreground/60"
            >
              소개
            </Link>
            {session && <Link href="/mypage">마이페이지</Link>}
            {session?.user?.email === process.env.NEXT_PUBLIC_ADMIN_EMAIL && (
              <Link href="/admin">관리자</Link>
            )}
          </nav>
        </div>
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <nav className="flex items-center">
            <ThemeToggle />
            {status === "authenticated" ? (
              <Button size="sm" variant="outline" onClick={() => signOut()}>로그아웃</Button>
            ) : (
              <Button size="sm" onClick={() => signIn("google")}>로그인</Button>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header; 