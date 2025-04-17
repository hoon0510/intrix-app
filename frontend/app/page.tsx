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
    <main>
      <div className="min-h-screen">
        <h1 className="text-4xl font-bold text-center py-8">Intrix 홈페이지</h1>
        <p className="text-center text-gray-600">
          감정과 욕구를 분석하여 최적의 마케팅 전략을 제공합니다.
        </p>
      </div>
    </main>
  );
} 