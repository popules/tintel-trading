"use client";

import React from "react";

export default function Card({ stock }: { stock: any }) {
  const { symbol, name, price, ai_score, flag, currency, why_summary } = stock;

  // AI färg (röd→orange→grön)
  const getColor = (score: number) => {
    if (score >= 80) return "text-green-400";
    if (score >= 65) return "text-yellow-400";
    return "text-red-400";
  };

  return (
    <div className="bg-neutral-900 rounded-2xl p-4 shadow-sm hover:bg-neutral-800 transition">
      <div className="flex justify-between items-center">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-lg font-semibold text-white">
              {flag} {symbol}
            </span>
          </div>
          <div className="text-xs text-neutral-400">{name}</div>
        </div>
        <div className="text-right">
          <div className="text-lg font-semibold text-white">
            {currency}{price ? price.toFixed(2) : "—"}
          </div>
          <div className={`text-sm ${getColor(ai_score)}`}>AI {ai_score}</div>
        </div>
      </div>
      <div className="text-xs text-neutral-400 mt-2">{why_summary}</div>
    </div>
  );
}
