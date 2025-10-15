"use client";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { getTicker } from "@/lib/api";
import Card from "@/components/Card";
import RadarChartComp from "@/components/RadarChart";
import Sparkline from "@/components/Sparkline";

function fmtMoney(v: any, exchange?: string) {
  const n = typeof v === "number" ? v : Number(v);
  if (!isFinite(n)) return "—";
  const isSEK = (exchange || "").toUpperCase() === "ST";
  return isSEK ? `${n.toFixed(2)} kr` : `$${n.toFixed(2)}`;
}

export default function TickerPage() {
  const params = useParams<{symbol: string}>();
  const sym = decodeURIComponent((params?.symbol || "")).toUpperCase();
  const [d, setD] = useState<any | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    getTicker(sym).then(setD).catch((e)=>{ setErr(String(e)); setD(null); });
  }, [sym]);

  if (err) return <div className="text-rose-300">{err}</div>;
  if (!d) return <div>loading…</div>;

  const badgeClass = /Undervärderad/.test(d.valuation_label)
    ? "border-emerald-400/30 text-emerald-300"
    : /Övervärderad/.test(d.valuation_label)
    ? "border-rose-400/30 text-rose-300"
    : "border-white/10 text-mute";

  return (
    <div className="space-y-6">
      <div className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-semibold">{d.symbol} <span className="text-mute text-lg">— {d.name}</span></h1>
          <div className="text-mute text-sm">{d.exchange} · {d.sector || "—"}</div>
        </div>
        <div className="text-right">
          <div className="text-3xl">{fmtMoney(d.price, d.exchange)}</div>
          <div className="text-mute text-sm">AI {d.ai_score}</div>
        </div>
      </div>

      <div className={`inline-block text-xs px-2 py-1 rounded-full border ${badgeClass}`}>{d.valuation_label}</div>

      <Card>
        <Sparkline data={d.spark || []} />
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 text-sm">
          <div>RSI14 <div className="text-lg">{d.rsi14 ?? "—"}</div></div>
          <div>EMA5 <div className="text-lg">{d.ema5 ? d.ema5.toFixed(2) : "—"}</div></div>
          <div>EMA20 <div className="text-lg">{d.ema20 ? d.ema20.toFixed(2) : "—"}</div></div>
          <div>EMA50 <div className="text-lg">{d.ema50 ? d.ema50.toFixed(2) : "—"}</div></div>
        </div>
      </Card>

      <div className="grid md:grid-cols-2 gap-4">
        <Card>
          <h3 className="font-semibold mb-2">factor radar</h3>
          {d.factors ? <RadarChartComp factors={d.factors}/> : <div className="text-mute text-sm">—</div>}
        </Card>
        <Card>
          <h3 className="font-semibold mb-2">quality snapshot</h3>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div>EV/Sales <div className="text-lg">{d.ev_sales ?? "—"}</div></div>
            <div>Revenue TTM YoY <div className="text-lg">{typeof d.revenue_ttm_yoy === "number" ? (d.revenue_ttm_yoy*100).toFixed(1)+"%" : "—"}</div></div>
            <div>Float <div className="text-lg">{d.float ? (d.float/1e6).toFixed(0)+"M" : "—"}</div></div>
            <div>ADV(20d) <div className="text-lg">{d.adv20 ? (d.adv20/1e6).toFixed(1)+"M" : "—"}</div></div>
          </div>
        </Card>
      </div>
    </div>
  );
}
