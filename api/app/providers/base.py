from typing import Protocol, Iterable

class MarketProvider(Protocol):
    async def list_candidates(self) -> Iterable[dict]:
        ...

    async def fetch_ticker_detail(self, symbol: str) -> dict:
        ...
