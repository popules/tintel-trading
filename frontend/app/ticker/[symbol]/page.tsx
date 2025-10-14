"use client";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { getTicker } from "@/lib/api";
import Card from "@/components/Card";
import RadarChartComp from "@/components/RadarChart";
import Sparkline from "@/components/Sparkline";

export default function TickerPage() {
  const params = useParams<{symbol: string}>();
  const sym = (params?.symbol || "").toUpperCase();
  const [d, setD] = useState<any | null>(null);
  useEffect(() => { getTicker(sym).then(setD).catch(()=>setD(null)); }, [sym]);

  if (!d) return <div>loading...</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-semibold">{sym} <span className="text-mute text-lg">— {d.name}</span></h1>
          <div className="text-mute text-sm">{d.exchange} · {d.sector || "—"}</div>
        </div>
        <div className="text-right">
          <div className="text-3xl">${d.price?.toFixed(2)}</div>
          <div className="text-mute text-sm">AI {d.ai_score}</div>
        </div>
      </div>

      <Card>
        <Sparkline data={d.spark || []} />
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 text-sm">
          <div>RSI14 <div className="text-lg">{d.rsi14 ? d.rsi14.toFixed(1) : "—"}</div></div>
          <div>EMA5 <div className="text-lg">{d.ema5 ? d.ema5.toFixed(2) : "—"}</div></div>
          <div>EMA20 <div className="text-lg">{d.ema20 ? d.ema20.toFixed(2) : "—"}</div></div>
          <div>EMA50 <div className="text-lg">{d.ema50 ? d.ema50.toFixed(2) : "—"}</div></div>
        </div>
      </Card>

      <div className="grid md:grid-cols-2 gap-4">
        <Card>
          <h3 className="font-semibold mb-2">factor radar</h3>
          <RadarChartComp factors={d.factors}/>
        </Card>
        <Card>
          <h3 className="font-semibold mb-2">quality snapshot</h3>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div>EV/Sales <div className="text-lg">{d.ev_sales ?? "—"}</div></div>
            <div>Revenue TTM YoY <div className="text-lg">{d.revenue_ttm_yoy ?? "—"}</div></div>
            <div>Float <div className="text-lg">{d.float ? (d.float/1e6).toFixed(0)+"M" : "—"}</div></div>
            <div>ADV(20d) <div className="text-lg">{d.adv20 ? (d.adv20/1e6).toFixed(1)+"M" : "—"}</div></div>
          </div>
        </Card>
      </div>
    </div>
  );
}
