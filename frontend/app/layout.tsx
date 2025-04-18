"use client";

import "./globals.css";
import { Inter } from "next/font/google";
import Navbar from "@/components/ui/navbar";
import Footer from "@/components/Footer";
import { ReactNode } from "react";
import Header from "@/components/Header";
import { ThemeProvider } from "@/components/theme-provider";
import { SessionProvider } from "next-auth/react";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="ko" suppressHydrationWarning>
      <body className={inter.className}>
        <SessionProvider>
          <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
          >
            <Header />
            <main className="flex-1">{children}</main>
            <Footer />
          </ThemeProvider>
        </SessionProvider>
      </body>
    </html>
  );
} 