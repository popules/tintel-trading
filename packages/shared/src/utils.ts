export const fmtUsd = (n?: number | null) =>
  typeof n === "number" ? `$${n.toLocaleString(undefined, { maximumFractionDigits: 2 })}` : "—";

export const pct = (x?: number | null) =>
  typeof x === "number" ? `${(x * 100).toFixed(1)}%` : "—";
