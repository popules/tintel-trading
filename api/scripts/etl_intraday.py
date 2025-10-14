"""
Fetch intraday prices/volume, compute volume Z and RSI, store in DailyMetrics.
In mock-mode, seeds a few rows for local dev.
"""
import asyncio
from sqlmodel import Session, select
from app.db import engine
from app.models import Ticker, DailyMetrics
from app.utils.indicators import rsi14
from datetime import date
import random

async def run():
    with Session(engine) as s:
        tickers = s.exec(select(Ticker)).all()
        for t in tickers:
            prices = [max(0.1, (t.price or 2) * (1 + random.uniform(-0.02, 0.02))) for _ in range(30)]
            rsi = rsi14(prices) or 50.0
            dm = DailyMetrics(
                symbol=t.symbol,
                date=date.today(),
                rsi14=rsi,
                momentum_score=min(1.0, max(0.0, (rsi - 30)/50)),
                volume_z=random.uniform(-1.0, 3.0),
            )
            s.add(dm)
        s.commit()

if __name__ == "__main__":
    asyncio.run(run())
