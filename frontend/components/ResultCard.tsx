import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";

interface ResultCardProps {
  resultId: string;
  title: string;
  description: string;
  createdAt: string;
}

export default function ResultCard({ resultId, title, description, createdAt }: ResultCardProps) {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-gray-500">생성일: {createdAt}</p>
      </CardContent>
      <CardFooter>
        <Button asChild className="w-full">
          <Link href={`/share/${resultId}`}>
            결과 보기
          </Link>
        </Button>
      </CardFooter>
    </Card>
  );
} 