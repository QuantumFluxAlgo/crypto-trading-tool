# app/crud/crud.py

from sqlalchemy.orm import Session
from app.models.models import Coin, MarketData, SentimentData
from datetime import datetime

def get_coins(db: Session):
    """
    Return all Coin records.
    """
    return db.query(Coin).all()

def upsert_coin(db: Session, symbol: str, name: str, source: str, last_updated: datetime) -> Coin:
    """
    Create or update a Coin.
    """
    coin = db.query(Coin).filter_by(symbol=symbol).first()
    if coin:
        coin.name = name
        coin.source = source
        coin.last_updated = last_updated
    else:
        coin = Coin(symbol=symbol, name=name, source=source, last_updated=last_updated)
        db.add(coin)

    db.commit()
    db.refresh(coin)
    return coin

def store_market_data(
    db: Session,
    coin_id: int,
    timestamp: datetime,
    price_usd: float,
    market_cap: float,
    volume_24h: float,
    source: str
):
    """
    Insert a new MarketData row.
    """
    md = MarketData(
        coin_id=coin_id,
        timestamp=timestamp,
        price_usd=price_usd,
        market_cap=market_cap,
        volume_24h=volume_24h,
        source=source
    )
    db.add(md)
    db.commit()

def store_sentiment_data(
    db: Session,
    coin_id: int,
    timestamp: datetime,
    galaxy_score: float,
    alt_rank: int,
    tweet_volume: int,
    social_score: float
):
    """
    Insert a new SentimentData row.
    """
    sd = SentimentData(
        coin_id=coin_id,
        timestamp=timestamp,
        galaxy_score=galaxy_score,
        alt_rank=alt_rank,
        tweet_volume=tweet_volume,
        social_score=social_score
    )
    db.add(sd)
    db.commit()

