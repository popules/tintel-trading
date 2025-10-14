import asyncio
from datetime import datetime, timedelta
from typing import Iterable
import yfinance as yf

class YahooProvider:
    async def list_candidates(self) -> Iterable[dict]:
        # Baseline universe approximation using popular lists as fallback
        # In production, store universe in DB and refresh nightly.
        tickers = ["AAPL","AMD","SOFI","CHPT","NOK","F","WISH","BBBYQ"]  # placeholder; filtered later/mocked
        out = []
        for t in tickers:
            try:
                y = yf.Ticker(t).info
                price = y.get("currentPrice") or y.get("regularMarketPrice")
                out.append({
                    "symbol": t,
                    "name": y.get("shortName") or t,
                    "exchange": (y.get("exchange") or "").upper(),
                    "sector": y.get("sector"),
                    "price": price,
                    "market_cap": y.get("marketCap"),
                    "float": y.get("floatShares"),
                    "adv20": (y.get("averageDailyVolume10Day") or y.get("averageVolume")) and float(y.get("averageVolume")),
                    "revenue_ttm": y.get("totalRevenue"),
                    "ev_sales": y.get("enterpriseToRevenue"),
                    "updated_at": datetime.utcnow().isoformat()
                })
            except Exception:
                continue
        return out

    async def fetch_ticker_detail(self, symbol: str) -> dict:
        y = yf.Ticker(symbol)
        info = y.info
        hist = y.history(period="1mo", interval="1d")
        spark = hist["Close"].tolist()[-30:]
        return {
            "symbol": symbol,
            "name": info.get("shortName") or symbol,
            "exchange": (info.get("exchange") or "").upper(),
            "sector": info.get("sector"),
            "price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "market_cap": info.get("marketCap"),
            "float": info.get("floatShares"),
            "adv20": float(info.get("averageVolume")) if info.get("averageVolume") else None,
            "revenue_ttm": info.get("totalRevenue"),
            "ev_sales": info.get("enterpriseToRevenue"),
            "spark": spark,
        }
