# app/api/v1/endpoints.py
from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
import app.db.session as db_session
from app.crud.crud import get_coins
from app.core.security import api_key_auth

router = APIRouter(prefix="/api/v1")

def get_db():
    db = db_session.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/coins", dependencies=[Depends(RateLimiter(times=20, minutes=1))])
async def read_coins(db: Session = Depends(get_db)) -> list[dict]:
    """Fetch all coins and return them as JSON-serializable dicts."""
    coins = get_coins(db)
    return [
        {
            "id": c.id,
            "symbol": c.symbol,
            "name": c.name,
            "source": c.source,
            "last_updated": c.last_updated.isoformat() if c.last_updated else None
        }
        for c in coins
    ]
