"use client";
import { useEffect, useRef, useState } from "react";
import { searchStocks } from "@/lib/api";
import Link from "next/link";

export default function Search({ market, onMarket }: { market: "US"|"ST"|"ALL"; onMarket: (m:"US"|"ST"|"ALL")=>void }) {
  const [q, setQ] = useState("");
  const [res, setRes] = useState<any[]>([]);
  const [open, setOpen] = useState(false);
  const timer = useRef<number | null>(null);

  useEffect(() => {
    if (!q.trim()) { setRes([]); setOpen(false); return; }
    if (timer.current) window.clearTimeout(timer.current);
    timer.current = window.setTimeout(async () => {
      try {
        const out = await searchStocks(q.trim(), market);
        setRes(out.results || []);
        setOpen(true);
      } catch {
        setRes([]);
        setOpen(false);
      }
    }, 250);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [q, market]);

  return (
    <div className="relative w-full max-w-xl">
      <div className="flex gap-2">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Sök aktie"
          autoComplete="off"
          spellCheck={false}
          name="tintel-search"
          className="w-full bg-card/60 border border-white/10 rounded-xl px-3 py-2 outline-none focus:border-white/20"
        />
        <select
          value={market}
          onChange={(e)=> onMarket(e.target.value as any)}
          className="bg-card/60 border border-white/10 rounded-xl px-3 py-2 text-sm"
        >
          <option value="ALL">ALL</option>
          <option value="US">🇺🇸 US</option>
          <option value="ST">🇸🇪 ST</option>
        </select>
      </div>

      {open && res.length > 0 && (
        <div className="absolute z-20 mt-1 w-full bg-card/90 border border-white/10 rounded-xl max-h-72 overflow-auto">
          {res.map((r) => (
            <Link key={r.symbol} href={`/ticker/${encodeURIComponent(r.symbol)}`} onClick={()=>setOpen(false)} className="block px-3 py-2 hover:bg-white/5">
              <div className="font-semibold">{r.symbol}</div>
              <div className="text-xs text-mute">{r.name} · {r.exchange}</div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
