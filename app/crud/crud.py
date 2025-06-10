from sqlalchemy.orm import Session
from app.models.models import Coin, MarketData, SentimentData

def get_coins(db: Session):
    return db.query(Coin).all()

# Extend with create/update functions and data validation as needed
