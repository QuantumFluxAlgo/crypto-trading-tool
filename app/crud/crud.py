# app/crud/crud.py
from sqlalchemy.orm import Session
from app.models.models import Coin, MarketData, SentimentData, PortfolioPosition
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
    user: str,
    exchange: str,
    asset_symbol: str,
    quantity: float,
    cost_basis: float,
    timestamp: datetime,
    realized_gain: float = 0.0,
) -> Portfolio:
    """Create or update a Portfolio row."""
    portfolio = (
        db.query(Portfolio)
        .filter_by(user=user, exchange=exchange, asset_symbol=asset_symbol)
        .first()
    )
    if portfolio:
        portfolio.quantity = quantity
        portfolio.cost_basis = cost_basis
        portfolio.timestamp = timestamp
        portfolio.realized_gain = realized_gain
    else:
        portfolio = Portfolio(
            user=user,
            exchange=exchange,
            asset_symbol=asset_symbol,
            quantity=quantity,
            cost_basis=cost_basis,
            timestamp=timestamp,
            realized_gain=realized_gain,
        )
        db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio


def create_transaction(
    db: Session,
    portfolio_id: int,
    user: str,
    exchange: str,
    asset_symbol: str,
    quantity: float,
    cost_basis: float,
    timestamp: datetime,
    realized_gain: float,
) -> Transaction:
    """Insert a new Transaction row."""
    tx = Transaction(
        portfolio_id=portfolio_id,
        user=user,
        exchange=exchange,
        asset_symbol=asset_symbol,
        quantity=quantity,
        cost_basis=cost_basis,
        timestamp=timestamp,
        realized_gain=realized_gain,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def get_portfolios_by_user(db: Session, user: str):
    """Return all portfolios for a user."""
    return db.query(Portfolio).filter_by(user=user).all()


def create_portfolio_position(
    db: Session,
    coin_id: int,
    exchange: str,
    quantity: float,
    avg_price: float,
    realized_pnl: float = 0.0,
) -> PortfolioPosition:
    pos = PortfolioPosition(
        coin_id=coin_id,
        exchange=exchange,
        quantity=quantity,
        avg_price=avg_price,
        realized_pnl=realized_pnl,
    )
    db.add(pos)
    db.commit()
    db.refresh(pos)
    return pos


def get_portfolio_positions(db: Session):
    return db.query(PortfolioPosition).all()


def get_latest_market_price(db: Session, coin_id: int) -> MarketData | None:
    return (
        db.query(MarketData)
        .filter_by(coin_id=coin_id)
        .order_by(MarketData.timestamp.desc())
        .first()
    )

