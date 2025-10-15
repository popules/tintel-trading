import os
import requests

API_KEY = os.getenv("FINNHUB_API_KEY", "")

def fetch_finnhub_quote(symbol: str):
    """Fallback Finnhub quote"""
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return {}
        d = r.json()
        return {
            "name": symbol,
            "price": d.get("c", 0.0),
            "pct_chg": d.get("dp", 0.0),
        }
    except Exception:
        return {"name": symbol, "price": 0.0, "pct_chg": 0.0}
