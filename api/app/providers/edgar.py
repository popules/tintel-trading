import httpx
from datetime import datetime, timedelta

class EdgarHook:
    async def insider_90d_net(self, symbol: str) -> float | None:
        # Simple RSS parsing via sec api RSS endpoint
        url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={symbol}&type=4&owner=only&count=40&output=atom"
        headers = {"User-Agent": "tintel/0.1 contact admin@tintel.se"}
        async with httpx.AsyncClient(timeout=15, headers=headers) as c:
            r = await c.get(url)
            if r.status_code != 200:
                return None
            text = r.text.lower()
            buys = text.count("acquisition")
            sells = text.count("disposition")
            # very rough net signal in 0..1 space
            total = max(1, buys + sells)
            return (buys - sells) / total * 0.5 + 0.5
