# app/crud/crud.py
from sqlalchemy.orm import Session

from app.models.models import Coin, MarketData, SentimentData, PortfolioPosition
    Coin,
    MarketData,
    SentimentData,
    Portfolio,
    PortfolioAsset,

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



def get_all_portfolios(db: Session) -> list[Portfolio]:
    return db.query(Portfolio).all()


def get_portfolio(db: Session, portfolio_id: int) -> Portfolio | None:
    return db.query(Portfolio).filter_by(id=portfolio_id).first()


def get_portfolio_assets(db: Session, portfolio_id: int) -> list[PortfolioAsset]:
    return db.query(PortfolioAsset).filter_by(portfolio_id=portfolio_id).all()