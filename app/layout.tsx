"use client";

import { Inter } from "next/font/google";
import "./globals.css";
import { SessionProvider } from "next-auth/react";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { usePathname } from "next/navigation";
import Link from "next/link";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  const isAuthPage = pathname === "/login" || pathname === "/register";
  const isSharePage = pathname.startsWith("/share/");
  const isAdminPage = pathname.startsWith("/admin");

  return (
    <html lang="en">
      <body className={inter.className}>
        <SessionProvider>
          {!isAuthPage && !isSharePage && !isAdminPage && (
            <nav className="bg-white shadow-sm">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16">
                  <div className="flex">
                    <div className="flex-shrink-0 flex items-center">
                      <Link href="/" className="text-xl font-bold text-gray-900">
                        Intrix
                      </Link>
                    </div>
                    <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                      <Link
                        href="/dashboard"
                        className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                          pathname === "/dashboard"
                            ? "border-blue-500 text-gray-900"
                            : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700"
                        }`}
                      >
                        대시보드
                      </Link>
                      <Link
                        href="/my-analysis"
                        className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                          pathname === "/my-analysis"
                            ? "border-blue-500 text-gray-900"
                            : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700"
                        }`}
                      >
                        내 분석
                      </Link>
                      <Link
                        href="/developer"
                        className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                          pathname === "/developer"
                            ? "border-blue-500 text-gray-900"
                            : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700"
                        }`}
                      >
                        개발자 포털
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            </nav>
          )}

          <main className="min-h-screen bg-gray-50">
            {children}
          </main>

          <ToastContainer
            position="top-right"
            autoClose={3000}
            hideProgressBar={false}
            newestOnTop
            closeOnClick
            rtl={false}
            pauseOnFocusLoss
            draggable
            pauseOnHover
          />
        </SessionProvider>
      </body>
    </html>
  );
} 