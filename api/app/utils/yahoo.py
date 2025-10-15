import yfinance as yf

def fetch_yahoo_quote(symbol: str):
    """Fetch quote safely from Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.fast_info
        return {
            "name": ticker.info.get("shortName", symbol),
            "price": float(info.get("last_price") or 0.0),
            "pct_chg": float(info.get("regularMarketChangePercent") or 0.0),
        }
    except Exception:
        return {"name": symbol, "price": 0.0, "pct_chg": 0.0}
