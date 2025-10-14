import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export default function Sparkline({ data }: { data: number[] }) {
  const series = data.map((v, i) => ({ i, v }));
  return (
    <div className="h-24">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={series}>
          <XAxis dataKey="i" hide />
          <YAxis hide domain={["dataMin", "dataMax"]} />
          <Tooltip />
          <Line type="monotone" dataKey="v" dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
