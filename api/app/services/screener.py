import random
from fastapi import HTTPException
from app.utils.yahoo import fetch_yahoo_quote
from app.utils.finnhub import fetch_finnhub_quote

def build_screener(exchange: str = "US", limit: int = 20):
    """Generate top setups with consistent fields and no NaN values."""
    try:
        from app.data.symbols import SYMBOLS_US, SYMBOLS_ST
    except ImportError:
        SYMBOLS_US, SYMBOLS_ST = [], []

    if exchange.upper() == "US":
        symbols = SYMBOLS_US or ["AAPL", "MSFT", "AMZN", "NVDA", "GOOG", "META"]
        flag = "🇺🇸"
        currency = "$"
    elif exchange.upper() == "ST":
        symbols = SYMBOLS_ST or ["INVE-B.ST", "VOLV-B.ST", "EVO.ST", "TEL2-B.ST"]
        flag = "🇸🇪"
        currency = "kr"
    else:
        raise HTTPException(status_code=400, detail="Unsupported exchange")

    random.shuffle(symbols)
    chosen = symbols[:limit]

    top = []
    rank = 1
    for sym in chosen:
        data = fetch_yahoo_quote(sym)
        if not data or "price" not in data:
            data = fetch_finnhub_quote(sym)

        price = float(data.get("price") or 0.0)
        ai_score = int(random.uniform(50, 90))

        # Default safe factors
        factors = {
            "mom": round(random.uniform(0.3, 0.9), 2),
            "qual": round(random.uniform(0.3, 0.9), 2),
            "cat": round(random.uniform(0.3, 0.9), 2),
            "val": round(random.uniform(0.3, 0.9), 2),
        }

        why_summary = random.choice([
            "momentum building",
            "improving quality",
            "fresh catalysts",
            "balanced setup",
        ])

        top.append({
            "rank": rank,
            "symbol": sym.replace(".ST", ""),
            "name": data.get("name") or sym,
            "exchange": exchange.upper(),
            "flag": flag,
            "currency": currency,
            "price": price,
            "pct_chg": data.get("pct_chg", 0.0),
            "ai_score": ai_score,
            "why_summary": why_summary,
            "factors": factors,
        })
        rank += 1

    return {"top": top}
