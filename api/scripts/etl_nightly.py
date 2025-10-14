"""
Nightly ETL: refresh fundamentals, insiders, offerings, sentiments, and weekly snapshot.
"""
import asyncio, os, json
from sqlmodel import Session
from app.db import engine
from app.models import Ticker, Snapshot
from app.services.screener import build_screener

async def run(seed: bool = False):
    # generate a weekly snapshot payload using screener
    top, spec = await build_screener(speculation=True, limit=20)
    payload = {"top": top, "speculation": spec}
    with Session(engine) as s:
        snap = Snapshot(payload_json=json.dumps(payload))
        s.add(snap)
        if seed and not s.get(Ticker, "SOFI"):
            # seed a few tickers for intraday ETL and UI
            s.add(Ticker(symbol="SOFI", name="SoFi", exchange="NASDAQ", sector="Fin", price=3.2, market_cap=300e6, float=90e6, adv20=7e6, revenue_ttm=120e6, ev_sales=3.1))
            s.add(Ticker(symbol="NOK", name="Nokia", exchange="NYSE", sector="Comm", price=3.5, market_cap=18000e6, float=4000e6, adv20=30e6, revenue_ttm=20000e6, ev_sales=0.8))
        s.commit()

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--seed", action="store_true")
    args = p.parse_args()
    asyncio.run(run(seed=args.seed))
