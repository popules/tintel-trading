export const WEIGHTS = {
  momentum: 0.30,
  quality: 0.30,
  catalysts: 0.25,
  valuation: 0.15
} as const;

export function clamp01(x: number | null | undefined): number {
  if (x == null || Number.isNaN(x)) return 0;
  return Math.max(0, Math.min(1, x));
}

export function compute_ai_score(f: {
  momentum?: number | null;
  quality?: number | null;
  catalysts?: number | null;
  valuation?: number | null;
}) {
  const m = clamp01(f.momentum);
  const q = clamp01(f.quality);
  const c = clamp01(f.catalysts);
  const v = clamp01(f.valuation);

  const score01 =
    WEIGHTS.momentum * m +
    WEIGHTS.quality * q +
    WEIGHTS.catalysts * c +
    WEIGHTS.valuation * v;

  const score100 = Math.round(score01 * 100);

  const why = [
    m > 0.7 ? "momentum hot" : m > 0.5 ? "momentum building" : null,
    q > 0.7 ? "solid quality" : q > 0.5 ? "improving quality" : null,
    c > 0.6 ? "fresh catalysts" : null,
    v > 0.7 ? "undervalued" : null
  ]
    .filter(Boolean)
    .slice(0, 3)
    .join(" · ") || "balanced setup";

  return {
    score: score100,
    factors: { mom: m, qual: q, cat: c, val: v },
    why_summary: why.slice(0, 140)
  };
}
