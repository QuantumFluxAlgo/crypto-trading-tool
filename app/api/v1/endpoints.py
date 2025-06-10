from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.db.session as db_session
from app.crud.crud import get_coins

router = APIRouter(prefix="/api/v1")

def get_db():
    db = db_session.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/coins")
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

