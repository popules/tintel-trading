from fastapi import APIRouter, Query
from ..services.screener import build_screener

router = APIRouter()

@router.get("/screener")
async def screener(speculation: bool = Query(default=False), limit: int = Query(default=20, ge=1, le=50)):
    top, spec = await build_screener(speculation=speculation, limit=limit)
    out = {"top": top}
    if speculation:
        out["speculation"] = spec
    return out
