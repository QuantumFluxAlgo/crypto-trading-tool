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
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class PortfolioAsset(Base):
    __tablename__ = "portfolio_assets"
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    coin_id = Column(Integer, ForeignKey("coins.id"))
    quantity = Column(Numeric)
    portfolio = relationship("Portfolio")
    coin = relationship("Coin")

