from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class FactorBreakdown(BaseModel):
    mom: float
    qual: float
    cat: float
    val: float

class ScreenerItem(BaseModel):
    symbol: str
    name: str
    price: float
    pct_chg: float
    rsi14: Optional[float] = None
    volume_z: Optional[float] = None
    si_pct_float: Optional[float] = None
    ev_sales: Optional[float] = None
    revenue_ttm_yoy: Optional[float] = None
    insider_net_90d: Optional[float] = None
    last_offering_date: Optional[str] = None
    ai_score: int
    factors: FactorBreakdown
    why_summary: str
    exchange: Optional[str] = None
    sector: Optional[str] = None

class ScreenerResponse(BaseModel):
    top: List[ScreenerItem]
    speculation: Optional[List[ScreenerItem]] = None

class TickerDetail(ScreenerItem):
    market_cap: Optional[float] = None
    float: Optional[float] = None
    adv20: Optional[float] = None
    ema5: Optional[float] = None
    ema20: Optional[float] = None
    ema50: Optional[float] = None
    spark: Optional[list[float]] = None
    quality_snapshot: Optional[Dict[str, Any]] = None
    insiders: Optional[list[dict]] = None
    offerings: Optional[list[dict]] = None
    si_available: Optional[bool] = None
