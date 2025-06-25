import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.crud.crud import get_coins, upsert_coin, store_market_data, store_sentiment_data
from app.models.models import Coin, MarketData, SentimentData

# Shared in-memory SQLite DB
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    Base.metadata.create_all(bind=engine)
    monkeypatch.setattr('app.db.session.SessionLocal', TestingSessionLocal)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_read_coins_empty():
    resp = client.get("/api/v1/coins")
    assert resp.status_code == 200
    assert resp.json() == []

def test_read_coins_with_data():
    db = TestingSessionLocal()
    now = datetime.utcnow()
    upsert_coin(db, "btc", "Bitcoin", "coingecko", now)
    upsert_coin(db, "eth", "Ethereum", "coinmarketcap", now)
    db.close()

    resp = client.get("/api/v1/coins")
    assert resp.status_code == 200
    symbols = {c["symbol"] for c in resp.json()}
    assert symbols == {"btc", "eth"}

def test_upsert_coin_creates_and_updates():
    db = TestingSessionLocal()
    now = datetime.utcnow()
    coin = upsert_coin(db, "ltc", "Litecoin", "coingecko", now)
    assert coin.symbol == "ltc"
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
        coin.id,
        now,
        0.5,
        500_000_000.0,
        10_000_000.0,
        high_24h=0.6,
        low_24h=0.4,
        price_change_24h=0.05,
        price_change_percentage_24h=10.0,
        percent_change_1h=1.0,
        percent_change_24h=2.0,
        source="coingecko",
    )
    result = db.query(MarketData).filter_by(coin_id=coin.id).first()
    assert float(result.open_24h) == 0.45
    assert float(result.high_24h) == 0.6
    assert float(result.percent_change_1h) == 1.0
    db.close()

def test_store_sentiment_data():
    db = TestingSessionLocal()
    now = datetime.utcnow()
    coin = upsert_coin(db, "doge", "Dogecoin", "lunarcrush", now)
    store_sentiment_data(db, coin.id, now, 20.0, 2, 5000, 15.0)
    result = db.query(SentimentData).filter_by(coin_id=coin.id).first()
    assert float(result.galaxy_score) == 20.0
    db.close()

