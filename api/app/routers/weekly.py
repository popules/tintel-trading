from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..db import get_session
from ..services.weekly import list_snapshots, create_snapshot

router = APIRouter()

@router.get("/weekly")
def weekly_list(session: Session = Depends(get_session)):
    return list_snapshots(session)

@router.post("/weekly")
def weekly_create(payload: dict, session: Session = Depends(get_session)):
    return create_snapshot(session, payload)
