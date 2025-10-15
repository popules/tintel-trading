from fastapi import APIRouter, Query
import httpx
import os

router = APIRouter()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "d3nb3hhr01qo7510ak0gd3nb3hhr01qo7510ak10")

@router.get("/search")
async def search_stocks(q: str = Query(..., min_length=1), exchange: str = Query("US")):
    """
    Sök aktier via Finnhub, med fallback till Yahoo Finance om Finnhub saknar resultat.
    """
    results = []
    async with httpx.AsyncClient() as client:

        # === 1️⃣ Försök via Finnhub ===
        finnhub_url = "https://finnhub.io/api/v1/search"
        params = {"q": q, "exchange": exchange, "token": FINNHUB_API_KEY}

        try:
            r = await client.get(finnhub_url, params=params, timeout=10)
            if r.status_code == 200:
                data = r.json()
                for d in data.get("result", []):
                    symbol = d.get("symbol")
                    name = d.get("description")
                    exch = d.get("exchange")
                    country = "US" if exch == "US" else "SE" if exch == "ST" else "🌍"
                    flag = "🇺🇸" if country == "US" else "🇸🇪" if country == "SE" else "🌍"

                    results.append({
                        "symbol": symbol,
                        "name": name,
                        "exchange": exch,
                        "flag": flag
                    })
        except Exception as e:
            print(f"Finnhub error: {e}")

        # === 2️⃣ Om inga resultat → kör Yahoo fallback ===
        if not results:
            yahoo_url = "https://query1.finance.yahoo.com/v1/finance/search"
            try:
                yr = await client.get(yahoo_url, params={"q": q, "lang": "en-US", "region": "US"}, timeout=10)
                if yr.status_code == 200:
                    data = yr.json()
                    for quote in data.get("quotes", []):
                        symbol = quote.get("symbol")
                        name = quote.get("shortname") or quote.get("longname") or symbol
                        exch = quote.get("exchange", "")
                        country = "US" if "NMS" in exch or "NYSE" in exch else \
                                  "SE" if "STO" in exch or "Stockholm" in exch else "🌍"
                        flag = "🇺🇸" if country == "US" else "🇸🇪" if country == "SE" else "🌍"

                        results.append({
                            "symbol": symbol,
                            "name": name,
                            "exchange": exch,
                            "flag": flag
                        })
                else:
                    print(f"Yahoo search failed: {yr.status_code}")
            except Exception as e:
                print(f"Yahoo error: {e}")

        return {"results": results}
