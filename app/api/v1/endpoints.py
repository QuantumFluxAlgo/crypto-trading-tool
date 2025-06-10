from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.crud.crud import get_coins

router = APIRouter(prefix="/api/v1")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/coins")
async def read_coins(db: Session = Depends(get_db)):
    return get_coins(db)
