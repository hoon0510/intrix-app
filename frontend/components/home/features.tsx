import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Brain, BarChart3, FileText, Users } from "lucide-react";

export default function Features() {
  const features = [
    {
      title: "감정 분석",
      description: "AI가 텍스트에서 감정을 분석하고, 욕구 구조를 파악합니다.",
      icon: "🎯"
    },
    {
      title: "전략 생성",
      description: "분석된 데이터를 바탕으로 최적의 마케팅 전략을 생성합니다.",
      icon: "🚀"
    },
    {
      title: "실행 가이드",
      description: "생성된 전략을 바탕으로 구체적인 실행 방안을 제시합니다.",
      icon: "📊"
    }
  ];

  return (
    <section id="features" className="w-full py-20 bg-white">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">주요 기능</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="p-6 rounded-xl bg-gray-50 hover:bg-gray-100 transition">
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
} 