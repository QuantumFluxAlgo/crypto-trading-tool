# app/crud/crud.py
from sqlalchemy.orm import Session
from app.models.models import (
    Coin,
    MarketData,
    SentimentData,
    Portfolio,
    Transaction,
)
from datetime import datetime

def get_coins(db: Session):
    """Return all Coin records."""
    return db.query(Coin).all()

def upsert_coin(db: Session, symbol: str, name: str, source: str, last_updated: datetime) -> Coin:
    """Create or update a Coin."""
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
    *,
    open_24h: float | None = None,
    high_24h: float | None = None,
    low_24h: float | None = None,
    price_change_24h: float | None = None,
    price_change_percentage_24h: float | None = None,
    percent_change_1h: float | None = None,
    percent_change_24h: float | None = None,
    source: str,
):
    """Insert a new MarketData row."""
    
    if open_24h is None and price_change_24h is not None:
        open_24h = price_usd - price_change_24h

    md = MarketData(
        coin_id=coin_id,
        timestamp=timestamp,
        price_usd=price_usd,
        market_cap=market_cap,
        volume_24h=volume_24h,
        open_24h=open_24h,
        high_24h=high_24h,
        low_24h=low_24h,
        price_change_24h=price_change_24h,
        price_change_percentage_24h=price_change_percentage_24h,
        percent_change_1h=percent_change_1h,
        percent_change_24h=percent_change_24h,
        source=source,
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
    """Insert a new SentimentData row."""
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


def upsert_portfolio(
    db: Session,
    coin_id: int,
    quantity: float,
    timestamp: datetime,
    source: str,
) -> Portfolio:
    """Create or update a Portfolio entry."""
    pf = (
        db.query(Portfolio)
        .filter_by(coin_id=coin_id, timestamp=timestamp)
        .first()
    )
    if pf:
        pf.quantity = quantity
        pf.source = source
    else:
        pf = Portfolio(
            coin_id=coin_id,
            quantity=quantity,
            timestamp=timestamp,
            source=source,
        )
        db.add(pf)
    db.commit()
    db.refresh(pf)
    return pf


def store_transaction(
    db: Session,
    coin_id: int,
    timestamp: datetime,
    amount: float,
    tx_type: str,
    price_usd: float,
    *,
    fee_usd: float | None = None,
    source: str,
) -> Transaction:
    """Insert a new Transaction row."""
    tx = Transaction(
        coin_id=coin_id,
        timestamp=timestamp,
        amount=amount,
        tx_type=tx_type,
        price_usd=price_usd,
        fee_usd=fee_usd,
        source=source,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

