"use client";

import React from "react";
import { Button } from "@/components/ui/button";
import { DownloadIcon } from "lucide-react";

interface DownloadSectionProps {
  downloadUrl: string;
}

const DownloadSection: React.FC<DownloadSectionProps> = ({ downloadUrl }) => {
  const handleDownload = () => {
    window.open(downloadUrl, "_blank");
  };

  return (
    <div className="w-full flex justify-end mt-6">
      <Button onClick={handleDownload} className="flex items-center gap-2">
        <DownloadIcon className="w-4 h-4" />
        PDF 다운로드
      </Button>
    </div>
  );
};

export default DownloadSection; 