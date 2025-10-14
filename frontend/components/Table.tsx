import Link from "next/link";

export default function Table({ rows, title }: { rows: any[]; title?: string }) {
  return (
    <div className="bg-card/60 rounded-2xl border border-white/5 overflow-hidden">
      {title && <div className="px-4 py-2 border-b border-white/5 text-sm text-mute">{title}</div>}
      <table className="w-full text-sm">
        <thead className="text-left text-mute">
          <tr>
            <th className="px-4 py-2">Symbol</th>
            <th>Name</th>
            <th>Price</th>
            <th>AI</th>
            <th>Mom</th>
            <th>Qual</th>
            <th>Cat</th>
            <th>Val</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.symbol} className="hover:bg-white/5">
              <td className="px-4 py-2 font-semibold"><Link href={`/ticker/${r.symbol}`}>{r.symbol}</Link></td>
              <td>{r.name}</td>
              <td>${r.price?.toFixed?.(2) ?? r.price}</td>
              <td>{r.ai_score}</td>
              <td>{(r.factors?.mom * 100).toFixed?.(0) || "—"}</td>
              <td>{(r.factors?.qual * 100).toFixed?.(0) || "—"}</td>
              <td>{(r.factors?.cat * 100).toFixed?.(0) || "—"}</td>
              <td>{(r.factors?.val * 100).toFixed?.(0) || "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
