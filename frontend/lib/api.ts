const BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export async function getScreener({ speculation=false, limit=20 } = {}) {
  const r = await fetch(`${BASE}/screener?speculation=${speculation}&limit=${limit}`, { next: { revalidate: 60 } });
  if (!r.ok) throw new Error("screener failed");
  return r.json();
}

export async function getTicker(symbol: string) {
  const r = await fetch(`${BASE}/ticker/${symbol}`, { cache: "no-store" });
  if (!r.ok) throw new Error("ticker failed");
  return r.json();
}

export async function getWeekly() {
  const r = await fetch(`${BASE}/weekly`, { next: { revalidate: 300 } });
  if (!r.ok) throw new Error("weekly failed");
  return r.json();
}
