"use client";

import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";

interface DownloadButtonProps {
  content: string;
  filename?: string;
}

export default function DownloadButton({ 
  content, 
  filename = "strategy_report.pdf" 
}: DownloadButtonProps) {
  const handleDownload = () => {
    const blob = new Blob([content], { type: "application/pdf" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <Button 
      onClick={handleDownload}
      className="flex items-center gap-2"
    >
      <Download className="w-4 h-4" />
      PDF 다운로드
    </Button>
  );
} 