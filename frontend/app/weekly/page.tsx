"use client";
import { useEffect, useState } from "react";
import { getWeekly } from "@/lib/api";
import Card from "@/components/Card";

export default function Weekly() {
  const [snaps, setSnaps] = useState<any[]>([]);
  useEffect(() => { getWeekly().then(setSnaps).catch(()=>setSnaps([])); }, []);
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">weekly radar</h1>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {snaps.map(s => (
          <Card key={s.id}>
            <div className="flex items-center justify-between">
              <div className="font-semibold">{new Date(s.created_at).toLocaleString()}</div>
              <div className="text-mute text-sm">{s.payload.top.length} picks</div>
            </div>
            <ul className="text-sm mt-2 space-y-1">
              {s.payload.top.slice(0,8).map((t:any)=>(
                <li key={t.symbol}><a className="hover:text-brand" href={`/ticker/${t.symbol}`}>{t.symbol}</a> — {t.why_summary}</li>
              ))}
            </ul>
          </Card>
        ))}
      </div>
    </div>
  );
}
