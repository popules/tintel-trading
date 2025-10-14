from fastapi import APIRouter
from ..services.ticker import get_ticker

router = APIRouter()

@router.get("/ticker/{symbol}")
async def ticker(symbol: str):
    return await get_ticker(symbol.upper())
