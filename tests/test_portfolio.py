import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.crud.crud import upsert_portfolio, create_transaction, get_portfolios_by_user
from app.models.models import Portfolio, Transaction

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
    monkeypatch.setattr("app.db.session.SessionLocal", TestingSessionLocal)
    yield
    Base.metadata.drop_all(bind=engine)


def test_upsert_and_get_portfolio():
    db = TestingSessionLocal()
    now = datetime.utcnow()
    upsert_portfolio(db, "alice", "binance", "BTC", 1.5, 10000.0, now)
    portfolios = get_portfolios_by_user(db, "alice")
    assert len(portfolios) == 1
    p = portfolios[0]
    assert p.asset_symbol == "BTC"
    assert float(p.quantity) == 1.5
    db.close()


def test_create_transaction():
    db = TestingSessionLocal()
    now = datetime.utcnow()
    portfolio = upsert_portfolio(db, "bob", "coinbase", "ETH", 2.0, 2000.0, now)
    tx = create_transaction(db, portfolio.id, "bob", "coinbase", "ETH", 1.0, 1000.0, now, 50.0)
    assert tx.portfolio_id == portfolio.id
    assert float(tx.realized_gain) == 50.0
    db.close()
