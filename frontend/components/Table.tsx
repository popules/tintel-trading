"use client";

import React from "react";

export default function Table({ data }: { data: any[] }) {
  const getColor = (score: number) => {
    if (score >= 80) return "text-green-400";
    if (score >= 65) return "text-yellow-400";
    return "text-red-400";
  };

  return (
    <div className="mt-6 bg-neutral-900 rounded-2xl p-3">
      <table className="min-w-full text-sm text-left text-neutral-300">
        <thead>
          <tr className="border-b border-neutral-700">
            <th className="py-2">Rank</th>
            <th className="py-2">Symbol</th>
            <th className="py-2">Name</th>
            <th className="py-2 text-right">Price</th>
            <th className="py-2 text-right">AI</th>
            <th className="py-2">Why</th>
          </tr>
        </thead>
        <tbody>
          {data.map((s) => (
            <tr key={s.symbol} className="border-b border-neutral-800 hover:bg-neutral-800">
              <td className="py-2">{s.rank}</td>
              <td className="py-2">{s.flag} {s.symbol}</td>
              <td className="py-2">{s.name}</td>
              <td className="py-2 text-right">
                {s.currency}{s.price ? s.price.toFixed(2) : "—"}
              </td>
              <td className={`py-2 text-right font-semibold ${getColor(s.ai_score)}`}>
                {s.ai_score}
              </td>
              <td className="py-2">{s.why_summary}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
