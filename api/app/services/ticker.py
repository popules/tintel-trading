from ..providers.mock import MockProvider
from ..providers.yahoo import YahooProvider
from ..providers.finnhub import FinnhubHooks
from ..providers.news import NewsHook
from ..providers.edgar import EdgarHook
from ..scoring import compute_ai_score
from ..utils.indicators import rsi14
import os
import numpy as np

def choose_provider():
    if os.getenv("MOCK", "0") == "1":
        return MockProvider()
    return YahooProvider()

async def get_ticker(symbol: str):
    provider = choose_provider()
    finnhub = FinnhubHooks()
    news = NewsHook()
    edgar = EdgarHook()

    d = await provider.fetch_ticker_detail(symbol)
    si = await finnhub.short_interest(symbol)
    sentiment = await news.sentiment(symbol) or 0.5
    insider = await edgar.insider_90d_net(symbol) or 0.5

    prices = d.get("spark") or []
    ema = lambda n: float(np.convolve(prices, np.ones(n)/n, mode="valid")[-1]) if len(prices) >= n else None

    momentum = 0.6 if (len(prices) > 2 and prices[-1] > prices[-2]) else 0.4
    quality = 0.5
    catalysts = sentiment
    valuation = 0.6 if d.get("ev_sales") and d["ev_sales"] < 3 else 0.4
    ai = compute_ai_score(momentum, quality, catalysts, valuation)

    return {
        "symbol": d["symbol"],
        "name": d["name"],
        "price": d.get("price"),
        "pct_chg": 0.0,
        "rsi14": rsi14(prices),
        "volume_z": None,
        "si_pct_float": si.get("si_pct_float"),
        "ev_sales": d.get("ev_sales"),
        "revenue_ttm_yoy": None,
        "insider_net_90d": round((insider - 0.5)*2, 2),
        "last_offering_date": None,
        "ai_score": ai.score,
        "factors": ai.factors,
        "why_summary": ai.why_summary,
        "exchange": d.get("exchange"),
        "sector": d.get("sector"),
        "market_cap": d.get("market_cap"),
        "float": d.get("float"),
        "adv20": d.get("adv20"),
        "ema5": ema(5),
        "ema20": ema(20),
        "ema50": ema(50),
        "spark": prices,
        "quality_snapshot": {
            "rev_ttm": d.get("revenue_ttm"),
            "ev/sales": d.get("ev_sales"),
        },
        "insiders": [],
        "offerings": [],
        "si_available": si.get("si_available", False)
    }
