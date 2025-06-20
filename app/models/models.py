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
