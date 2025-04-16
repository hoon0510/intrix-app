"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";
import { ChevronDown, ChevronUp, Star, Eye, Trash2 } from "lucide-react";
import { FavoriteItem } from "../types/favorite";
import AnalysisResult from "./AnalysisResult";

export default function FavoriteList() {
  const [favorites, setFavorites] = useState<FavoriteItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const { data: session } = useSession();
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());

  useEffect(() => {
    if (session) {
      fetchFavorites();
    }
  }, [session]);

  const fetchFavorites = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/favorites`);
      if (!response.ok) {
        throw new Error("Failed to fetch favorites");
      }
      const data = await response.json();
      setFavorites(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  const handleItemClick = (item: FavoriteItem) => {
    router.push(`/analysis/${item.analysis_id}`);
  };

  const handleDelete = async (id: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/favorites/${id}`, {
        method: "DELETE",
      });
      if (!response.ok) {
        throw new Error("Failed to delete favorite");
      }
      setFavorites(favorites.filter((fav) => fav.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    }
  };

  const toggleExpand = (id: string) => {
    setExpandedItems((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center text-red-600">
        <svg
          className="mx-auto h-12 w-12 text-red-500"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <p className="mt-2">{error}</p>
      </div>
    );
  }

  if (favorites.length === 0) {
    return (
      <div className="text-center text-gray-500">
        <Star className="mx-auto h-12 w-12 text-gray-400" />
        <p className="mt-2">No favorites yet</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {favorites.map((favorite) => (
        <div
          key={favorite.id}
          className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow"
        >
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <h3 className="text-lg font-semibold">{favorite.input_text}</h3>
              <p className="text-sm text-gray-400 mt-2">
                {new Date(favorite.created_at).toLocaleDateString()}
              </p>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => handleItemClick(favorite)}
                className="text-blue-600 hover:text-blue-800 p-2 rounded-full hover:bg-blue-50"
                title="View"
              >
                <Eye className="h-5 w-5" />
              </button>
              <button
                onClick={() => handleDelete(favorite.id)}
                className="text-red-600 hover:text-red-800 p-2 rounded-full hover:bg-red-50"
                title="Delete"
              >
                <Trash2 className="h-5 w-5" />
              </button>
              <button
                onClick={() => toggleExpand(favorite.id)}
                className="text-gray-600 hover:text-gray-800 p-2 rounded-full hover:bg-gray-50"
                title={expandedItems.has(favorite.id) ? "Collapse" : "Expand"}
              >
                {expandedItems.has(favorite.id) ? (
                  <ChevronUp className="h-5 w-5" />
                ) : (
                  <ChevronDown className="h-5 w-5" />
                )}
              </button>
            </div>
          </div>
          {expandedItems.has(favorite.id) && (
            <div className="mt-4">
              <AnalysisResult
                analysisId={favorite.analysis_id}
                inputText={favorite.input_text}
                result={favorite.result_json ? JSON.parse(favorite.result_json) : undefined}
                className="mt-4"
              />
            </div>
          )}
        </div>
      ))}
    </div>
  );
} 