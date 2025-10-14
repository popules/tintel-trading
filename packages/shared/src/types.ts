export type FactorBreakdown = {
  momentum: number; // 0..1
  quality: number;  // 0..1
  catalysts: number;// 0..1
  valuation: number;// 0..1
};

export type ScreenerItem = {
  symbol: string;
  name: string;
  price: number;
  pct_chg: number;
  rsi14: number | null;
  volume_z: number | null;
  si_pct_float?: number | null;
  ev_sales?: number | null;
  revenue_ttm_yoy?: number | null;
  insider_net_90d: number | null;
  last_offering_date?: string | null;
  ai_score: number; // 0..100
  factors: { mom: number; qual: number; cat: number; val: number };
  why_summary: string;
  exchange?: "NASDAQ" | "NYSE" | "AMEX";
  sector?: string | null;
};

export type ScreenerResponse = {
  top: ScreenerItem[];
  speculation?: ScreenerItem[];
};

export type TickerDetail = ScreenerItem & {
  market_cap?: number | null;
  float?: number | null;
  adv20?: number | null;
  ema5?: number | null;
  ema20?: number | null;
  ema50?: number | null;
  spark?: number[]; // recent prices
  quality_snapshot?: Record<string, number | string | null>;
  insiders?: Array<{ filed_at: string; insider_name: string; shares: number; value_usd: number; direction: "BUY"|"SELL" }>;
  offerings?: Array<{ date: string; type: string; amount_usd: number }>;
  si_available?: boolean;
};
