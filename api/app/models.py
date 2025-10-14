from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship

class Ticker(SQLModel, table=True):
    symbol: str = Field(primary_key=True, index=True)
    name: str
    exchange: str
    sector: str | None = None
    price: float | None = None
    market_cap: float | None = None
    float: float | None = None
    adv20: float | None = None
    revenue_ttm: float | None = None
    ev_sales: float | None = None
    updated_at: datetime | None = None

class DailyMetrics(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    symbol: str = Field(foreign_key="ticker.symbol", index=True)
    date: date
    rsi14: float | None = None
    momentum_score: float | None = None
    quality_score: float | None = None
    catalysts_score: float | None = None
    valuation_score: float | None = None
    ai_score: float | None = None
    volume_z: float | None = None

class Insider(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    symbol: str = Field(index=True)
    filed_at: date
    insider_name: str
    shares: int
    value_usd: float
    direction: str  # BUY/SELL

class Offering(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    symbol: str = Field(index=True)
    date: date
    type: str
    amount_usd: float

class Snapshot(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    payload_json: str
