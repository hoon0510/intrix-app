"use client";

import { useEffect, useState } from "react";
import { useSession } from "next-auth/react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import AuthGuard from "@/components/auth/AuthGuard";

interface Analysis {
  id: string;
  title: string;
  createdAt: string;
  isFavorite: boolean;
}

export default function Page() {
  const { data: session } = useSession();
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (session?.user?.email) {
      fetchAnalyses();
    }
  }, [session]);

  const fetchAnalyses = async () => {
    try {
      const response = await fetch(`/api/analyses?email=${session?.user?.email}`);
      if (!response.ok) throw new Error("Failed to fetch analyses");
      const data = await response.json();
      setAnalyses(data);
    } catch (error) {
      toast.error("Failed to load analyses");
    } finally {
      setLoading(false);
    }
  };

  const toggleFavorite = async (id: string) => {
    try {
      const response = await fetch(`/api/analyses/${id}/favorite`, {
        method: "POST",
      });
      if (!response.ok) throw new Error("Failed to toggle favorite");
      setAnalyses((prev) =>
        prev.map((analysis) =>
          analysis.id === id
            ? { ...analysis, isFavorite: !analysis.isFavorite }
            : analysis
        )
      );
    } catch (error) {
      toast.error("Failed to update favorite status");
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardHeader>
            <CardTitle>My Account</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold">Email</h3>
                <p>{session?.user?.email}</p>
              </div>
              <div>
                <h3 className="font-semibold">Name</h3>
                <p>{session?.user?.name}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Analysis History</CardTitle>
          </CardHeader>
          <CardContent>
            {analyses.length === 0 ? (
              <p>No analyses found</p>
            ) : (
              <div className="space-y-4">
                {analyses.map((analysis) => (
                  <div
                    key={analysis.id}
                    className="flex items-center justify-between p-4 border rounded"
                  >
                    <div>
                      <h4 className="font-semibold">{analysis.title}</h4>
                      <p className="text-sm text-gray-500">
                        {new Date(analysis.createdAt).toLocaleDateString()}
                      </p>
                    </div>
                    <Button
                      variant={analysis.isFavorite ? "default" : "outline"}
                      onClick={() => toggleFavorite(analysis.id)}
                    >
                      {analysis.isFavorite ? "Unfavorite" : "Favorite"}
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </AuthGuard>
  );
} 