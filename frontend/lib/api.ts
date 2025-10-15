const BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

export async function getScreener(params?: { exchange?: "US" | "ST"; limit?: number }) {
  const u = new URL(`${BASE}/screener`);
  if (params?.exchange) u.searchParams.set("exchange", params.exchange);
  if (params?.limit) u.searchParams.set("limit", String(params.limit));
  const r = await fetch(u.toString(), { cache: "no-store" });
  if (!r.ok) throw new Error(`screener failed: ${r.status}`);
  return r.json();
}

export async function getTicker(symbol: string) {
  const r = await fetch(`${BASE}/ticker/${encodeURIComponent(symbol)}`, { cache: "no-store" });
  if (!r.ok) throw new Error(`ticker failed: ${r.status}`);
  return r.json();
}

export async function searchStocks(q: string, market: "ALL" | "US" | "ST" = "ALL") {
  const u = new URL(`${BASE}/search`);
  u.searchParams.set("q", q);
  u.searchParams.set("market", market);
  const r = await fetch(u.toString(), { cache: "no-store" });
  if (!r.ok) throw new Error(`search failed: ${r.status}`);
  return r.json();
}
