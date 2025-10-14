import os
from typing import List, Tuple
from ..providers.mock import MockProvider
from ..providers.yahoo import YahooProvider
from ..providers.finnhub import FinnhubHooks
from ..providers.news import NewsHook
from ..providers.edgar import EdgarHook
from ..utils.filters import quality_gates
from ..scoring import compute_ai_score

def choose_provider():
    # Use Yahoo baseline unless MOCK=1
    if os.getenv("MOCK", "0") == "1":
        return MockProvider()
    return YahooProvider()

async def build_screener(speculation: bool, limit: int) -> Tuple[list, list]:
    provider = choose_provider()
    finnhub = FinnhubHooks()
    news = NewsHook()
    edgar = EdgarHook()

    raw = [x for x in await provider.list_candidates()]

    good, bad = [], []
    for r in raw:
        if quality_gates(r):
            good.append(r)
        else:
            bad.append(r)

    results = []
    for r in good:
        # pseudo factors
        momentum = 0.5
        quality = 0.5
        catalysts = await news.sentiment(r["symbol"]) or 0.4
        valuation = 0.5 if (r.get("ev_sales") and r["ev_sales"] < 4) else 0.3

        si = await finnhub.short_interest(r["symbol"])
        insider = await edgar.insider_90d_net(r["symbol"]) or 0.5

        ai = compute_ai_score(momentum, quality, catalysts, valuation)
        results.append({
            "symbol": r["symbol"],
            "name": r.get("name") or r["symbol"],
            "price": round(r.get("price") or 0, 2),
            "pct_chg": 0.0,
            "rsi14": None,
            "volume_z": None,
            "si_pct_float": si.get("si_pct_float"),
            "ev_sales": r.get("ev_sales"),
            "revenue_ttm_yoy": None,
            "insider_net_90d": round((insider - 0.5)*2, 2),  # -1..1-ish
            "last_offering_date": None,
            "ai_score": ai.score,
            "factors": ai.factors,
            "why_summary": ai.why_summary,
            "exchange": r.get("exchange"),
            "sector": r.get("sector"),
        })

    results.sort(key=lambda x: x["ai_score"], reverse=True)
    top = results[:limit]

    speculation_list = []
    if speculation:
        for r in bad[:limit]:
            ai = compute_ai_score(0.4, 0.2, 0.3, 0.2)
            speculation_list.append({
                "symbol": r["symbol"],
                "name": r.get("name") or r["symbol"],
                "price": round(r.get("price") or 0, 2),
                "pct_chg": 0.0,
                "rsi14": None,
                "volume_z": None,
                "si_pct_float": None,
                "ev_sales": r.get("ev_sales"),
                "revenue_ttm_yoy": None,
                "insider_net_90d": 0.0,
                "last_offering_date": None,
                "ai_score": ai.score,
                "factors": ai.factors,
                "why_summary": "speculation mode · risk HIGH",
                "exchange": r.get("exchange"),
                "sector": r.get("sector"),
                "risk": "HIGH"
            })

    return top, speculation_list
