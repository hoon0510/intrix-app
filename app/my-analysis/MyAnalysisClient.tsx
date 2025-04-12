'use client';

import React, { useState, useEffect } from 'react';
import { FavoriteButton } from '@/components/FavoriteButton';
import { useRouter } from 'next/navigation';
import { toast } from 'react-toastify';
import { motion, AnimatePresence } from 'framer-motion';

interface Analysis {
  id: string;
  date: string;
  channels: string[];
  copy: string;
  strategy_summary: string;
  style: string;
}

interface MyAnalysisClientProps {
  analyses: Analysis[];
}

export function MyAnalysisClient({ analyses }: MyAnalysisClientProps) {
  const router = useRouter();
  const [sortedAnalyses, setSortedAnalyses] = useState<Analysis[]>([]);
  const [favorites, setFavorites] = useState<Record<string, boolean>>({});
  const [loadingStates, setLoadingStates] = useState<Record<string, boolean>>({});
  const [showFavoritesOnly, setShowFavoritesOnly] = useState(false);
  const [isDownloading, setIsDownloading] = useState(false);
  const [downloadDisabledUntil, setDownloadDisabledUntil] = useState<number | null>(null);
  const [remainingTime, setRemainingTime] = useState<number | null>(null);

  // Format time in MM:SS
  const formatTime = (seconds: number): string => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  // Initialize countdown from localStorage
  useEffect(() => {
    const storedDisabledUntil = localStorage.getItem('downloadDisabledUntil');
    if (storedDisabledUntil) {
      const disabledUntil = parseInt(storedDisabledUntil, 10);
      const now = Date.now();
      
      if (disabledUntil > now) {
        setDownloadDisabledUntil(disabledUntil);
        setRemainingTime(Math.ceil((disabledUntil - now) / 1000));
      } else {
        // Clear expired timer
        localStorage.removeItem('downloadDisabledUntil');
      }
    }
  }, []);

  // Countdown timer effect
  useEffect(() => {
    if (!downloadDisabledUntil) {
      setRemainingTime(null);
      localStorage.removeItem('downloadDisabledUntil');
      return;
    }

    // Store the disabled time in localStorage
    localStorage.setItem('downloadDisabledUntil', downloadDisabledUntil.toString());

    const timer = setInterval(() => {
      const now = Date.now();
      const remaining = Math.ceil((downloadDisabledUntil - now) / 1000);
      
      if (remaining <= 0) {
        // Clean up when timer expires
        setDownloadDisabledUntil(null);
        setRemainingTime(null);
        localStorage.removeItem('downloadDisabledUntil');
        clearInterval(timer);
        
        // Show success toast when timer expires
        toast.success('다운로드가 다시 가능합니다', {
          autoClose: 3000,
          className: 'bg-green-50 border-l-4 border-green-400 text-green-700',
        });
      } else {
        setRemainingTime(remaining);
      }
    }, 1000);

    return () => {
      clearInterval(timer);
      // Clean up localStorage if component unmounts
      if (downloadDisabledUntil && Date.now() >= downloadDisabledUntil) {
        localStorage.removeItem('downloadDisabledUntil');
      }
    };
  }, [downloadDisabledUntil]);

  useEffect(() => {
    // Fetch favorite status for all analyses
    const fetchFavoriteStatuses = async () => {
      const statuses: Record<string, boolean> = {};
      
      for (const analysis of analyses) {
        try {
          const response = await fetch(`/api/favorite/status?user_id=user1&analysis_id=${analysis.id}`);
          if (response.ok) {
            const data = await response.json();
            statuses[analysis.id] = data.favorited;
          }
        } catch (error) {
          console.error(`Failed to fetch favorite status for analysis ${analysis.id}:`, error);
          statuses[analysis.id] = false;
        }
      }
      
      setFavorites(statuses);
    };

    fetchFavoriteStatuses();
  }, [analyses]);

  useEffect(() => {
    // Sort analyses with favorites first
    let filtered = [...analyses];
    
    // Filter favorites if enabled
    if (showFavoritesOnly) {
      filtered = filtered.filter(analysis => favorites[analysis.id]);
    }
    
    // Sort by favorite status and date
    const sorted = filtered.sort((a, b) => {
      const aIsFavorite = favorites[a.id] || false;
      const bIsFavorite = favorites[b.id] || false;
      
      if (aIsFavorite && !bIsFavorite) return -1;
      if (!aIsFavorite && bIsFavorite) return 1;
      
      // If both are favorited or not, sort by date
      return new Date(b.date).getTime() - new Date(a.date).getTime();
    });
    
    setSortedAnalyses(sorted);
  }, [analyses, favorites, showFavoritesOnly]);

  const handleToggleFavorite = async (analysisId: string) => {
    const isCurrentlyFavorite = favorites[analysisId];
    
    // Optimistically update UI
    setFavorites(prev => ({
      ...prev,
      [analysisId]: !isCurrentlyFavorite
    }));
    
    // Set loading state
    setLoadingStates(prev => ({
      ...prev,
      [analysisId]: true
    }));
    
    try {
      const response = await fetch(`/api/favorite/${analysisId}`, {
        method: isCurrentlyFavorite ? 'DELETE' : 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to update favorite status');
      }
      
      toast.success(
        isCurrentlyFavorite 
          ? '즐겨찾기에서 제거되었습니다'
          : '즐겨찾기에 추가되었습니다'
      );
    } catch (error) {
      // Rollback on error
      setFavorites(prev => ({
        ...prev,
        [analysisId]: isCurrentlyFavorite
      }));
      
      console.error('Error toggling favorite:', error);
      toast.error('즐겨찾기 상태 변경에 실패했습니다');
    } finally {
      // Clear loading state
      setLoadingStates(prev => ({
        ...prev,
        [analysisId]: false
      }));
    }
  };

  const handleAnalysisClick = (analysisId: string) => {
    router.push(`/result/${analysisId}`);
  };

  const toggleShowFavoritesOnly = () => {
    setShowFavoritesOnly(!showFavoritesOnly);
  };

  const handleBatchDownload = async () => {
    // Get favorited analysis IDs
    const favoritedIds = Object.entries(favorites)
      .filter(([_, isFavorited]) => isFavorited)
      .map(([id]) => id);

    if (favoritedIds.length === 0) {
      toast.warning('다운로드할 즐겨찾기 항목이 없습니다');
      return;
    }

    setIsDownloading(true);

    try {
      const response = await fetch('/api/download/favorites', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: 'user1' }), // TODO: Replace with actual user ID
      });

      if (!response.ok) {
        const errorData = await response.json();
        
        if (response.status === 429) {
          // Set disabled time to 10 minutes from now
          const disabledUntil = Date.now() + 600000; // 10 minutes in milliseconds
          setDownloadDisabledUntil(disabledUntil);
          
          // Handle rate limit error with distinct styling
          toast.error(
            <div className="flex flex-col gap-1">
              <span className="font-semibold">{errorData.error}</span>
              <span className="text-sm text-gray-600">
                남은 시간: {errorData.remaining_seconds}초
              </span>
            </div>,
            {
              className: 'bg-yellow-50 border-l-4 border-yellow-400 text-yellow-700',
              icon: '⏰',
              autoClose: 5000,
            }
          );
          return;
        }
        
        throw new Error(errorData.error || '다운로드 요청에 실패했습니다');
      }

      // Get the blob from the response
      const blob = await response.blob();
      
      // Create a URL for the blob
      const url = window.URL.createObjectURL(blob);
      
      // Create a temporary link element
      const a = document.createElement('a');
      a.href = url;
      a.download = `favorite_reports_user1.zip`; // TODO: Replace with actual user ID
      
      // Append to body, click, and remove
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      toast.success('즐겨찾기한 전략이 성공적으로 다운로드되었습니다');
    } catch (error) {
      console.error('Batch download failed:', error);
      toast.error('다운로드 중 오류가 발생했습니다');
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Filter Toggle and Download Button */}
      <div className="sticky top-0 z-10 bg-white p-4 rounded-lg shadow-sm mb-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">내 분석 목록</h2>
          <div className="flex items-center gap-4">
            <div className="relative group">
              <button
                onClick={handleBatchDownload}
                disabled={isDownloading || Object.values(favorites).filter(Boolean).length === 0 || downloadDisabledUntil !== null}
                className={`flex items-center space-x-2 px-4 py-2 rounded-full transition-colors ${
                  isDownloading || downloadDisabledUntil !== null
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-blue-100 text-blue-800 hover:bg-blue-200'
                }`}
                title={downloadDisabledUntil !== null ? "ZIP 다운로드는 10분에 1회만 가능합니다" : undefined}
              >
                {isDownloading ? (
                  <>
                    <svg className="animate-spin h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span>다운로드 중...</span>
                  </>
                ) : downloadDisabledUntil !== null && remainingTime !== null ? (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                    </svg>
                    <span className="flex items-center gap-1">
                      <span className="font-medium">다시 시도 가능:</span>
                      <span className="tabular-nums">{formatTime(remainingTime)}</span>
                    </span>
                  </>
                ) : (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                    <span>즐겨찾기한 전략 PDF 다운로드</span>
                  </>
                )}
              </button>
              {/* Desktop-only tooltip */}
              <div className="hidden md:block">
                {downloadDisabledUntil !== null && (
                  <div className="absolute left-1/2 -translate-x-1/2 -top-10 opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none">
                    <div className="bg-gray-800 text-white text-xs px-3 py-1 rounded-md whitespace-nowrap">
                      ZIP 다운로드는 10분에 1회만 가능합니다
                    </div>
                  </div>
                )}
              </div>
            </div>
            <button
              onClick={toggleShowFavoritesOnly}
              className={`flex items-center space-x-2 px-4 py-2 rounded-full transition-colors ${
                showFavoritesOnly
                  ? 'bg-blue-100 text-blue-800'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className={`h-5 w-5 ${
                  showFavoritesOnly ? 'text-blue-600' : 'text-gray-400'
                }`}
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M3.172 5.172a5.5 5.5 0 017.656 0L10 6.343l-.828-.171a5.5 5.5 0 00-7.656 0zM10 15l-1.414-1.414a3.5 3.5 0 00-4.95 0L2 15v3a1 1 0 001 1h14a1 1 0 001-1v-3l-1.586-1.586a3.5 3.5 0 00-4.95 0L10 15z"
                  clipRule="evenodd"
                />
              </svg>
              <span>즐겨찾기만 보기</span>
            </button>
          </div>
        </div>
      </div>

      {/* Analysis List */}
      <AnimatePresence mode="popLayout">
        {sortedAnalyses.length === 0 ? (
          <motion.div
            key="empty-state"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="text-center py-8"
          >
            <p className="text-gray-500">
              {showFavoritesOnly
                ? '즐겨찾기한 분석이 없습니다'
                : '분석 결과가 없습니다'}
            </p>
          </motion.div>
        ) : (
          <div className="space-y-4">
            {sortedAnalyses.map((analysis) => (
              <motion.div
                key={analysis.id}
                layout
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{
                  type: "spring",
                  stiffness: 500,
                  damping: 30,
                  mass: 1
                }}
                className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer"
                onClick={() => handleAnalysisClick(analysis.id)}
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {analysis.copy}
                      </h3>
                      {favorites[analysis.id] && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-gray-900">
                          <span className="mr-1">⭐</span>
                          고정됨
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-500 mt-1">
                      {new Date(analysis.date).toLocaleString()}
                    </p>
                  </div>
                  <div
                    onClick={(e) => {
                      e.stopPropagation();
                      handleToggleFavorite(analysis.id);
                    }}
                    className="relative"
                  >
                    <FavoriteButton 
                      isFavorite={favorites[analysis.id] || false} 
                      onClick={() => {}} 
                      isLoading={loadingStates[analysis.id] || false}
                    />
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-gray-700">채널:</span>
                    <div className="flex flex-wrap gap-2">
                      {analysis.channels.map((channel) => (
                        <span
                          key={channel}
                          className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs"
                        >
                          {channel}
                        </span>
                      ))}
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-gray-700">스타일:</span>
                    <span className="text-sm text-gray-600">{analysis.style}</span>
                  </div>
                  
                  <div className="mt-2">
                    <p className="text-sm text-gray-600 line-clamp-2">
                      {analysis.strategy_summary}
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </AnimatePresence>
    </div>
  );
} 