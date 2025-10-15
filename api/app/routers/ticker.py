from fastapi import APIRouter, HTTPException
import random

router = APIRouter()

@router.get("/ticker/{symbol}")
async def get_ticker(symbol: str):
    """
    Returnerar detaljer för en enskild aktie (mock tills vidare)
    """
    data = {
        "symbol": symbol.upper(),
        "name": symbol.upper(),
        "price": round(random.uniform(0.5, 1500), 2),
        "ai_score": random.randint(50, 95),
        "why_summary": random.choice(["balanced setup", "momentum building", "fresh catalysts"]),
        "sector": random.choice(["Tech", "Energy", "Finance", "AI"]),
        "exchange": "NASDAQ" if symbol.isupper() else "ST"
    }
    if not data:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return data
