-- init schema mirrors alembic; for bootstrap or manual psql
CREATE TABLE IF NOT EXISTS ticker (
  symbol TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  exchange TEXT NOT NULL,
  sector TEXT,
  price DOUBLE PRECISION,
  market_cap DOUBLE PRECISION,
  float DOUBLE PRECISION,
  adv20 DOUBLE PRECISION,
  revenue_ttm DOUBLE PRECISION,
  ev_sales DOUBLE PRECISION,
  updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dailymetrics (
  id SERIAL PRIMARY KEY,
  symbol TEXT REFERENCES ticker(symbol),
  date DATE NOT NULL,
  rsi14 DOUBLE PRECISION,
  momentum_score DOUBLE PRECISION,
  quality_score DOUBLE PRECISION,
  catalysts_score DOUBLE PRECISION,
  valuation_score DOUBLE PRECISION,
  ai_score DOUBLE PRECISION,
  volume_z DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS insider (
  id SERIAL PRIMARY KEY,
  symbol TEXT NOT NULL,
  filed_at DATE NOT NULL,
  insider_name TEXT NOT NULL,
  shares INTEGER NOT NULL,
  value_usd DOUBLE PRECISION NOT NULL,
  direction TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS offering (
  id SERIAL PRIMARY KEY,
  symbol TEXT NOT NULL,
  date DATE NOT NULL,
  type TEXT NOT NULL,
  amount_usd DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS snapshot (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  payload_json TEXT NOT NULL
);
