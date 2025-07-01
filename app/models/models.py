from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Coin(Base):
    __tablename__ = "coins"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    source = Column(String)
    last_updated = Column(DateTime)

class MarketData(Base):
    __tablename__ = "market_data"
    id = Column(Integer, primary_key=True, index=True)
    coin_id = Column(Integer, ForeignKey("coins.id"))
    timestamp = Column(DateTime)
    price_usd = Column(Numeric)
    market_cap = Column(Numeric)
    volume_24h = Column(Numeric)
    high_24h = Column(Numeric)
    low_24h = Column(Numeric)
    price_change_24h = Column(Numeric)
    price_change_percentage_24h = Column(Numeric)
    percent_change_1h = Column(Numeric)
    percent_change_24h = Column(Numeric)
    open_24h = Column(Numeric)
    source = Column(String)
    coin = relationship("Coin")

class SentimentData(Base):
    __tablename__ = "sentiment_data"
    id = Column(Integer, primary_key=True, index=True)
    coin_id = Column(Integer, ForeignKey("coins.id"))
    timestamp = Column(DateTime)
    galaxy_score = Column(Numeric)
    alt_rank = Column(Integer)
    tweet_volume = Column(Integer)
    social_score = Column(Numeric)
    coin = relationship("Coin")


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, index=True)
    exchange = Column(String)
    asset_symbol = Column(String, index=True)
    quantity = Column(Numeric)
    cost_basis = Column(Numeric)
    timestamp = Column(DateTime)
    realized_gain = Column(Numeric)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    user = Column(String, index=True)
    exchange = Column(String)
    asset_symbol = Column(String, index=True)
    quantity = Column(Numeric)
    cost_basis = Column(Numeric)
    timestamp = Column(DateTime)
    realized_gain = Column(Numeric)
    portfolio = relationship("Portfolio")


class PortfolioPosition(Base):
    __tablename__ = "portfolio_positions"
    id = Column(Integer, primary_key=True, index=True)
    coin_id = Column(Integer, ForeignKey("coins.id"))
    exchange = Column(String)
    quantity = Column(Numeric)
    avg_price = Column(Numeric)
    realized_pnl = Column(Numeric, default=0)
    coin = relationship("Coin")
