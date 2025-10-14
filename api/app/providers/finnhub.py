import httpx
import os

FINNHUB_URL = "https://finnhub.io/api/v1"

class FinnhubHooks:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("FINNHUB_API_KEY")

    async def short_interest(self, symbol: str):
        if not self.api_key:
            return {"si_available": False, "si_pct_float": None}
        url = f"{FINNHUB_URL}/stock/short-interest?symbol={symbol}&token={self.api_key}"
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url)
            if r.status_code != 200:
                return {"si_available": False, "si_pct_float": None}
            data = r.json()
            val = None
            try:
                val = (data["shortInterest"][0]["shortInterest"] / data["shortInterest"][0]["float"]) if data.get("shortInterest") else None
            except Exception:
                val = None
            return {"si_available": True, "si_pct_float": val}
