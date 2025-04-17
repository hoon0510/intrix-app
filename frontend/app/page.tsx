"use client";

import React from "react";
import Link from "next/link";
import Hero from "@/components/home/hero";
import Features from "@/components/home/features";
import HowItWorks from "@/components/home/how-it-works";
import HomeIntro from "@/components/home/HomeIntro";
import Footer from "@/components/common/Footer";
import FeatureGrid from "@/components/home/FeatureGrid";
import ContactForm from "@/components/ContactForm";
import CallToActionSection from "@/components/home/CallToActionSection";

export default function HomePage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Hero />
      <HomeIntro />
      <Features />
      <HowItWorks />
      <section className="py-20 bg-gray-50" id="contact">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">문의하기</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Intrix에 대해 궁금한 점이 있으신가요? 언제든지 문의주세요.
              빠른 시일 내에 답변 드리도록 하겠습니다.
            </p>
          </div>
          <ContactForm />
        </div>
      </section>
      <CallToActionSection />
      <section className="bg-gray-100 py-20 text-center">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold mb-4">Intrix를 지금 바로 시작해보세요</h2>
          <p className="text-lg text-gray-600 mb-6">로그인하고 리뷰 기반 전략 분석을 직접 경험해보세요.</p>
          <div className="flex justify-center space-x-4">
            <Link 
              href="/login" 
              className="px-6 py-3 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors"
            >
              로그인
            </Link>
            <Link 
              href="/signup" 
              className="px-6 py-3 bg-white text-black border border-black rounded-lg hover:bg-gray-100 transition-colors"
            >
              회원가입
            </Link>
          </div>
        </div>
      </section>
      <Footer />
    </div>
  );
} 