# tests/test_endpoints.py

import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.crud.crud import upsert_coin, store_market_data, store_sentiment_data
from app.models.models import Coin, MarketData, SentimentData

# ————————————————
# Set up an in-memory SQLite DB for tests
# ————————————————
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# Override the SessionLocal used by the app to point at our in-memory DB
@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    # Create all tables
    Base.metadata.create_all(bind=engine)
    # Override the SessionLocal factory
    monkeypatch.setattr("app.db.session.SessionLocal", TestingSessionLocal)
    yield
    # Teardown: drop all tables
    Base.metadata.drop_all(bind=engine)

# Instantiate TestClient after the override
client = TestClient(app)

# ————————————————
# Endpoint Tests
# ————————————————
def test_read_coins_empty():
    resp = client.get("/api/v1/coins")
    assert resp.status_code == 200
    assert resp.json() == []

def test_read_coins_with_data():
    # Seed two coins
    db = TestingSessionLocal()
    now = datetime.utcnow()
    upsert_coin(db, "btc", "Bitcoin", "coingecko", now)
    upsert_coin(db, "eth", "Ethereum", "coinmarketcap", now)
    db.close()

    resp = client.get("/api/v1/coins")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    symbols = {c["symbol"] for c in data}
    assert symbols == {"btc", "eth"}

# ————————————————
# CRUD Function Tests
# ————————————————
def test_upsert_coin_creates_and_updates():
    db = TestingSessionLocal()
    now = datetime.utcnow()
    # Create
    coin = upsert_coin(db, "ltc", "Litecoin", "coingecko", now)
    assert isinstance(coin, Coin)
    assert coin.symbol == "ltc"
    # Update
    later = datetime.utcnow()
    updated = upsert_coin(db, "ltc", "LitecoinX", "coingecko", later)
    assert updated.id == coin.id
    assert updated.name == "LitecoinX"
    db.close()

def test_store_market_data():
    db = TestingSessionLocal()
    now = datetime.utcnow()
    coin = upsert_coin(db, "xrp", "XRP", "coingecko", now)
    store_market_data(
        db,
        coin_id=coin.id,
        timestamp=now,
        price_usd=0.5,
        market_cap=500_000_000.0,
        volume_24h=10_000_000.0,
        source="coingecko"
    )
    result = db.query(MarketData).filter_by(coin_id=coin.id).first()
    assert result.price_usd == 0.5
    assert result.market_cap == 500_000_000.0
    assert result.volume_24h == 10_000_000.0
    db.close()

def test_store_sentiment_data():
    db = TestingSessionLocal()
    now = datetime.utcnow()
    coin = upsert_coin(db, "doge", "Dogecoin", "lunarcrush", now)
    store_sentiment_data(
        db,
        coin_id=coin.id,
        timestamp=now,
        galaxy_score=20.0,
        alt_rank=2,
        tweet_volume=5_000,
        social_score=15.0
    )
    result = db.query(SentimentData).filter_by(coin_id=coin.id).first()
    assert result.galaxy_score == 20.0
    assert result.alt_rank == 2
    assert result.tweet_volume == 5_000
    assert result.social_score == 15.0
    db.close()
