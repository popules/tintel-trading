from datetime import datetime, timedelta
import random

class MockProvider:
    async def list_candidates(self):
        symbols = ["SOFI","NOK","IONQ","PLUG","RIOT","MARA","CHPT","DNA","BBAI","CANO","AQB","BBBY","SPCE","RKLB","UPST"]
        out = []
        for s in symbols:
            price = round(random.uniform(0.5, 5.0), 2)
            out.append({
                "symbol": s, "name": s, "exchange": "NASDAQ", "sector": "Tech",
                "price": price, "market_cap": random.randint(120, 800)*1e6,
                "float": random.randint(25, 400)*1e6, "adv20": random.randint(3, 50)*1e6,
                "revenue_ttm": random.randint(30, 900)*1e6, "ev_sales": round(random.uniform(0.5, 8.0),2),
                "updated_at": datetime.utcnow().isoformat()
            })
        return out

    async def fetch_ticker_detail(self, symbol: str):
        import math
        spark = [round(2 + math.sin(i/3)*0.2 + random.random()*0.05, 2) for i in range(30)]
        return {
            "symbol": symbol, "name": symbol, "exchange": "NASDAQ", "sector": "Tech",
            "price": spark[-1], "market_cap": 300e6, "float": 80e6, "adv20": 6e6,
            "revenue_ttm": 120e6, "ev_sales": 3.2, "spark": spark
        }
