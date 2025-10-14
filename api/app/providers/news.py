import os, httpx

class NewsHook:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("NEWSAPI_KEY")

    async def sentiment(self, symbol: str) -> float | None:
        if not self.api_key:
            return None
        # naive sentiment proxy: count positive/negative titles via NewsAPI
        url = f"https://newsapi.org/v2/everything?q={symbol}&pageSize=10&apiKey={self.api_key}"
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(url)
            if r.status_code != 200:
                return None
            arts = r.json().get("articles", [])
            if not arts:
                return None
            pos = sum(1 for a in arts if any(w in (a["title"] or "").lower() for w in ["beat","surge","up","wins","contract","award"]))
            neg = sum(1 for a in arts if any(w in (a["title"] or "").lower() for w in ["miss","down","fell","lawsuit","delist","going concern"]))
            total = max(1, pos + neg)
            return (pos - neg) / total * 0.5 + 0.5  # map to 0..1
