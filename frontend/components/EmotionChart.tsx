"use client";

import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface EmotionChartData {
  labels: string[];
  values: number[];
}

interface EmotionChartProps {
  data: EmotionChartData;
}

export default function EmotionChart({ data }: EmotionChartProps) {
  const chartData = {
    labels: data.labels,
    datasets: [
      {
        label: "감정 강도",
        data: data.values,
        backgroundColor: "rgba(59, 130, 246, 0.5)",
        borderColor: "rgb(59, 130, 246)",
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        text: "감정 분석 결과",
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
      },
    },
  };

  return (
    <div className="w-full h-[400px] p-4 bg-white rounded-lg shadow-sm">
      <Bar data={chartData} options={options} />
    </div>
  );
} 