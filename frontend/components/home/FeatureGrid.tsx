import { Card, CardTitle, CardDescription } from "@/components/ui/card";

const features = [
  {
    title: "AI 기반 욕구 분석",
    description: "리뷰, 댓글 속 감정과 욕구를 정량화하여 사용자 의도를 파악합니다.",
  },
  {
    title: "자동 전략 생성",
    description: "감정과 욕구 기반 전환 전략을 자동으로 설계합니다.",
  },
  {
    title: "카피라이팅 자동화",
    description: "전략에 맞춘 강력한 본능 자극형 카피를 자동 생성합니다.",
  },
  {
    title: "브랜딩 전략 도출",
    description: "Reference Point 전환과 포지셔닝 전략까지 자동 설계합니다.",
  },
];

export default function FeatureGrid() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-6">
      {features.map((feature, idx) => (
        <Card key={idx} className="p-6 rounded-2xl shadow hover:shadow-lg transition-shadow">
          <CardTitle className="text-lg font-semibold">{feature.title}</CardTitle>
          <CardDescription className="mt-2 text-sm text-muted-foreground">
            {feature.description}
          </CardDescription>
        </Card>
      ))}
    </div>
  );
} 