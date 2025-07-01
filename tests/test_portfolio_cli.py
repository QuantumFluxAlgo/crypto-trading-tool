import pytest
from datetime import datetime
from typer.testing import CliRunner

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.crud.crud import (
    upsert_coin,
    store_market_data,
    create_portfolio_position,
)
from app.cli.portfolio_cli import app as cli_app

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
    monkeypatch.setattr("app.cli.portfolio_cli.SessionLocal", TestingSessionLocal)
    yield
    Base.metadata.drop_all(bind=engine)


def test_live_value():
    db = TestingSessionLocal()
    now = datetime.utcnow()
    coin = upsert_coin(db, "btc", "Bitcoin", "coingecko", now)
    store_market_data(db, coin.id, now, 10000, 1, 2, source="coingecko")
    create_portfolio_position(db, coin.id, "binance", 0.5, 9000)
    db.close()

    runner = CliRunner()
    result = runner.invoke(cli_app, ["live"])
    assert "$5,000" in result.stdout


def test_gains_and_summary():
    db = TestingSessionLocal()
    now = datetime.utcnow()
    coin = upsert_coin(db, "eth", "Ethereum", "coingecko", now)
    store_market_data(db, coin.id, now, 2000, 1, 2, source="coingecko")
    create_portfolio_position(db, coin.id, "kraken", 1, 1500, realized_pnl=100)
    db.close()

    runner = CliRunner()
    gains_out = runner.invoke(cli_app, ["gains"]).stdout
    assert "unrealized" in gains_out
    summary_out = runner.invoke(cli_app, ["summary"]).stdout
    assert "kraken" in summary_out
    assert "ETH" in summary_out
