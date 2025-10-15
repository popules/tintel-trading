from fastapi import APIRouter

router = APIRouter()

@router.get("/weekly")
async def weekly():
    return {"message": "weekly snapshots placeholder"}
