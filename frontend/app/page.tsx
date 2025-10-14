"use client";
import { useEffect, useState } from "react";
import { getScreener } from "@/lib/api";
import Card from "@/components/Card";
import Table from "@/components/Table";
import Toggle from "@/components/Toggle";
import FactorTooltip from "@/components/FactorTooltip";

export default function Dashboard() {
  const [spec, setSpec] = useState(false);
  const [data, setData] = useState<{top:any[];speculation?:any[]}>({top:[]});

  useEffect(() => {
    getScreener({ speculation: spec, limit: 20 }).then(setData).catch(() => setData({top:[]}));
  }, [spec]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">top setups</h1>
        <Toggle checked={spec} onChange={setSpec} label="speculation mode" />
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {data.top.slice(0, 12).map((t) => (
          <Card key={t.symbol}>
            <div className="flex items-center justify-between">
              <div>
                <a className="text-lg font-semibold hover:text-brand" href={`/ticker/${t.symbol}`}>{t.symbol}</a>
                <div className="text-mute text-sm">{t.name}</div>
              </div>
              <div className="text-right">
                <div className="text-xl">${t.price?.toFixed(2)}</div>
                <div className="text-mute text-xs">AI {t.ai_score}</div>
              </div>
            </div>
            <FactorTooltip factors={t.factors} why={t.why_summary} />
          </Card>
        ))}
      </div>

      <Table rows={data.top} title="Top 20" />

      {spec && data.speculation && (
        <>
          <h2 className="text-xl mt-8">speculation (risk: HIGH)</h2>
          <Table rows={data.speculation} title="Speculation" />
        </>
      )}
    </div>
  );
}
