import React from "react";

interface Props {
  slogans: string[];
}

export default function StrategySlogan({ slogans }: Props) {
  return (
    <div className="space-y-2 p-4 bg-gray-100 rounded-lg">
      <h2 className="text-xl font-semibold">추천 슬로건</h2>
      <ul className="list-disc list-inside text-gray-800">
        {slogans.map((slogan, idx) => (
          <li key={idx}>{slogan}</li>
        ))}
      </ul>
    </div>
  );
} 