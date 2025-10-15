from fastapi import APIRouter, Query
from ..config import settings
import typing as t, random, requests, yfinance as yf

router = APIRouter()

FINNHUB = settings.FINNHUB_API_KEY

SE_UNIVERSE = [
    ("ATCO-A.ST", "Atlas Copco A"), ("ATCO-B.ST", "Atlas Copco B"),
    ("ABB.ST", "ABB"), ("ERIC-B.ST", "Ericsson B"), ("NDA-SE.ST", "Nordea"),
    ("VOLV-B.ST", "Volvo B"), ("SAND.ST", "Sandvik"), ("ALFA.ST", "Alfa Laval"),
    ("HMB.ST", "H&M B"), ("TEL2-B.ST", "Tele2 B"), ("TELIA.ST", "Telia"),
    ("SKF-B.ST", "SKF B"), ("SCA-B.ST", "SCA B"), ("EVO.ST", "Evolution"),
    ("SEB-A.ST", "SEB A"), ("SWED-A.ST", "Swedbank A"), ("SHB-A.ST", "Handelsbanken A"),
    ("INVE-B.ST", "Investor B"), ("ASSA-B.ST", "ASSA ABLOY B"), ("SINCH.ST", "Sinch"),
    ("KINV-B.ST", "Kinnevik B"), ("HEXA-B.ST", "Hexagon B"), ("BOL.ST", "Boliden"),
    ("ELUX-B.ST", "Electrolux B"), ("SSAB-B.ST", "SSAB B"), ("EQT.ST", "EQT"),
]

def _ai_stub() -> tuple[int, str]:
    score = random.randint(50, 90)
    why = random.choice(["momentum building", "fresh catalysts", "improving quality", "balanced setup"])
    return score, why

def _pct(cur: float, prev: float) -> float:
    if not prev:
        return 0.0
    return round((cur - prev) / prev * 100.0, 2)

@router.get("/screener")
def screener(exchange: str = Query(default="US"), limit: int = Query(default=20, ge=1, le=100)):
    ex = (exchange or "US").strip().upper()

    # ---- USA via Finnhub ----
    if ex in {"US", "USA", "NYSE", "NASDAQ"}:
        if not FINNHUB:
            return {"error": "Missing FINNHUB_API_KEY", "top": []}
        try:
            res = requests.get(
                "https://finnhub.io/api/v1/stock/symbol",
                params={"exchange": "US", "token": FINNHUB}, timeout=15
            )
            res.raise_for_status()
            payload = [x for x in res.json() if isinstance(x, dict) and x.get("symbol")]
        except Exception as e:
            return {"error": f"symbol fetch failed: {e}", "top": []}

        sample = random.sample(payload, min(limit, len(payload)))
        out: list[dict] = []
        for tkr in sample:
            symbol = tkr["symbol"]
            name = tkr.get("description") or symbol
            try:
                q = requests.get(
                    "https://finnhub.io/api/v1/quote",
                    params={"symbol": symbol, "token": FINNHUB}, timeout=10
                ).json()
            except Exception:
                q = {}
            c = float(q.get("c") or 0.0)
            pc = float(q.get("pc") or 0.0)
            pct = _pct(c, pc)
            ai, why = _ai_stub()
            out.append({
                "symbol": symbol, "name": name, "exchange": "US",
                "price": c, "pct_chg": pct, "ai_score": ai, "why_summary": why,
            })
        return {"top": out}

    # ---- Sverige via yfinance ----
    if ex in {"SE", "ST", "STO", "SWE", "SWEDEN"}:
        rows: list[dict] = []
        for symbol, name in random.sample(SE_UNIVERSE, min(limit, len(SE_UNIVERSE))):
            try:
                y = yf.Ticker(symbol)
                hist = y.history(period="2d")
                price = float(hist["Close"].iloc[-1]) if not hist.empty else 0.0
                prev = float(hist["Close"].iloc[-2]) if len(hist) > 1 else 0.0
                if price == 0.0:
                    info = y.info or {}
                    price = float(info.get("currentPrice") or info.get("regularMarketPrice") or 0.0)
                    prev = float(info.get("previousClose") or prev)
            except Exception:
                price, prev = 0.0, 0.0
            pct = _pct(price, prev)
            ai, why = _ai_stub()
            rows.append({
                "symbol": symbol.replace(".ST",""),
                "name": name,
                "exchange": "ST",
                "price": price,
                "pct_chg": pct,
                "ai_score": ai,
                "why_summary": why,
            })
        return {"top": rows}

    return {"error": f"unsupported exchange '{exchange}'", "top": []}
