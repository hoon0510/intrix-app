"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import AuthGuard from "@/components/auth/AuthGuard";

interface AnalysisResult {
  id: string;
  title: string;
  content: string;
  createdAt: string;
}

export default function Page() {
  const params = useParams();
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchResult();
  }, [params.id]);

  const fetchResult = async () => {
    try {
      const response = await fetch(`/api/analyze/${params.id}`);
      if (!response.ok) throw new Error("Failed to fetch analysis result");
      const data = await response.json();
      setResult(data);
    } catch (error) {
      toast.error("Failed to load analysis result");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-red-500">Analysis result not found</p>
      </div>
    );
  }

  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardHeader>
            <CardTitle>{result.title}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold">Analysis Content</h3>
                <p className="whitespace-pre-wrap">{result.content}</p>
              </div>
              <div>
                <h3 className="font-semibold">Created At</h3>
                <p>{new Date(result.createdAt).toLocaleString()}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <div className="mt-4">
          <Button onClick={() => window.history.back()}>Back</Button>
        </div>
      </div>
    </AuthGuard>
  );
} 