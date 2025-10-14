import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer } from "recharts";

export default function RadarChartComp({ factors }: { factors: { mom:number; qual:number; cat:number; val:number }}) {
  const data = [
    { k: "Momentum", v: factors.mom },
    { k: "Quality", v: factors.qual },
    { k: "Catalysts", v: factors.cat },
    { k: "Valuation", v: factors.val },
  ];
  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="k" />
          <Radar dataKey="v" strokeWidth={2} fillOpacity={0.2} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
