import { cn } from "@/lib/utils";

interface SkeletonProps {
  className?: string;
  width?: string | number;
  height?: string | number;
  rounded?: "none" | "sm" | "md" | "lg" | "full";
}

const Skeleton = ({ 
  className, 
  width = "100%", 
  height = "1rem",
  rounded = "md"
}: SkeletonProps) => {
  const roundedClass = {
    none: "rounded-none",
    sm: "rounded-sm",
    md: "rounded-md",
    lg: "rounded-lg",
    full: "rounded-full"
  }[rounded];

  return (
    <div
      className={cn(
        "animate-pulse bg-muted",
        roundedClass,
        className
      )}
      style={{ 
        width: typeof width === "number" ? `${width}px` : width,
        height: typeof height === "number" ? `${height}px` : height,
        opacity: 0.3 
      }}
    />
  );
};

export { Skeleton }; 