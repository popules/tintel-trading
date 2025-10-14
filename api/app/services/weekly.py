from sqlmodel import select, Session
from ..models import Snapshot
from datetime import datetime
import json

def create_snapshot(session: Session, payload: dict):
    snap = Snapshot(payload_json=json.dumps(payload, separators=(",",":")))
    session.add(snap)
    session.commit()
    session.refresh(snap)
    return {"id": snap.id, "created_at": snap.created_at.isoformat()}

def list_snapshots(session: Session, limit: int = 12):
    q = select(Snapshot).order_by(Snapshot.created_at.desc()).limit(limit)
    snaps = session.exec(q).all()
    return [
        {"id": s.id, "created_at": s.created_at.isoformat(), "payload": json.loads(s.payload_json)}
        for s in snaps
    ]
