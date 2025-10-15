import yfinance as yf
import requests
import numpy as np
from datetime import datetime, timedelta

FINNHUB_KEY = None  # Finnhub-quote fallback om satt via env i routers/screener eller globalt

def _rsi14(closes):
    if len(closes) < 15:
        return None
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)
    avg_gain = gains[:14].mean()
    avg_loss = losses[:14].mean()
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    # Wilder smoothing
    for i in range(14, len(deltas)):
        gain = gains[i]
        loss = losses[i]
        avg_gain = (avg_gain * 13 + gain) / 14
        avg_loss = (avg_loss * 13 + loss) / 14
        rs = avg_gain / (avg_loss if avg_loss != 0 else 1e-9)
        rsi = 100.0 - (100.0 / (1.0 + rs))
    return float(round(rsi, 1))

def _ema(series, n):
    if len(series) < n:
        return None
    return float(np.array(series).astype(float)[-n:].mean())

def _ai_score(rsi, ev_sales, yoy):
    # Enkel, robust modell för demo
    score = 50
    if rsi is not None:
        if rsi < 30: score += 10
        elif rsi > 70: score -= 10
        elif 40 <= rsi <= 60: score += 5
    if ev_sales is not None:
        if ev_sales < 2: score += 7
        elif ev_sales > 6: score -= 5
    if yoy is not None:
        if yoy > 0.1: score += 8
        elif yoy < -0.1: score -= 6
    return int(max(0, min(100, score)))

def _valuation_label(score):
    if score >= 70:
        return "Undervärderad enligt Tintel"
    if score <= 40:
        return "Övervärderad enligt Tintel"
    return "Rimligt värde enligt Tintel"

def _finnhub_quote(symbol):
    if not FINNHUB_KEY:
        return None
    try:
        r = requests.get("https://finnhub.io/api/v1/quote", params={"symbol": symbol, "token": FINNHUB_KEY}, timeout=8)
        if r.status_code != 200:
            return None
        j = r.json()
        c = j.get("c")
        d = j.get("d")
        dp = j.get("dp")
        if not c:
            return None
        return {"price": float(c), "pct_chg": float(dp) if dp is not None else None}
    except Exception:
        return None

def _yahoo_detail(symbol: str):
    y = yf.Ticker(symbol)
    info = y.info or {}

    price = info.get("currentPrice") or info.get("regularMarketPrice")
    # Sparkline (30 senaste stängningar)
    hist = y.history(period="1mo", interval="1d")
    closes = hist["Close"].tolist() if "Close" in hist else []
    spark = [float(round(x, 4)) for x in closes[-30:]] if closes else []

    rsi = _rsi14(closes) if closes else None
    ema5 = _ema(closes, 5) if closes else None
    ema20 = _ema(closes, 20) if closes else None
    ema50 = _ema(closes, 50) if closes else None

    name = info.get("shortName") or info.get("longName") or symbol
    exchange = (info.get("exchange") or "").upper()
    sector = info.get("sector")

    ev_sales = info.get("enterpriseToRevenue")  # EV/Sales
    revenue_ttm = info.get("totalRevenue")
    revenue_yoy = info.get("revenueGrowth")  # fraction e.g. 0.12
    market_cap = info.get("marketCap")
    float_shares = info.get("floatShares") or info.get("sharesFloat")
    adv20 = info.get("averageVolume") or info.get("averageDailyVolume10Day")

    pct_chg = info.get("regularMarketChangePercent")
    if pct_chg is not None:
        try:
            pct_chg = float(pct_chg)
        except Exception:
            pct_chg = None

    return {
        "symbol": symbol,
        "name": name,
        "price": float(price) if price is not None else None,
        "pct_chg": pct_chg,
        "rsi14": rsi,
        "exchange": exchange,
        "sector": sector,
        "market_cap": market_cap,
        "float": float_shares,
        "adv20": adv20,
        "ev_sales": ev_sales,
        "revenue_ttm_yoy": float(revenue_yoy) if revenue_yoy is not None else None,
        "spark": spark,
        "ema5": ema5,
        "ema20": ema20,
        "ema50": ema50,
    }

def get_ticker_detail(symbol: str):
    # 1) Yahoo som bas (global täckning inkl .ST)
    d = _yahoo_detail(symbol)

    # 2) Finnhub-quote override (bättre %chg ibland på US)
    q = _finnhub_quote(symbol)
    if q and q.get("price"):
        d["price"] = q["price"]
        if q.get("pct_chg") is not None:
            d["pct_chg"] = q["pct_chg"]

    # 3) AI-score + valuation
    score = _ai_score(d.get("rsi14"), d.get("ev_sales"), d.get("revenue_ttm_yoy"))
    d["ai_score"] = score
    d["valuation_label"] = _valuation_label(score)

    # 4) Factors (enkelt, 0..1)
    mom = 0.5
    if d.get("rsi14") is not None:
        r = d["rsi14"]
        mom = 1 - abs(50 - r) / 50  # nära 50 = 1.0, extremt = lägre
    qual = 0.6 if (d.get("revenue_ttm_yoy") or 0) > 0 else 0.4
    cat = 0.6 if (d.get("pct_chg") or 0) > 0 else 0.4
    val = 0.7 if (d.get("ev_sales") or 9e9) < 2 else (0.5 if (d.get("ev_sales") or 0) < 4 else 0.3)
    d["factors"] = {"mom": float(round(mom, 2)), "qual": qual, "cat": cat, "val": val}

    # Why-summary kort
    why = []
    if mom > 0.6: why.append("momentum building")
    if qual > 0.55: why.append("improving quality")
    if cat > 0.55: why.append("fresh catalysts")
    if val > 0.6: why.append("undervalued")
    d["why_summary"] = " · ".join(why) or "balanced setup"

    # Meta
    d["si_pct_float"] = None
    d["insider_net_90d"] = None
    d["last_offering_date"] = None
    d["si_available"] = False

    return d
