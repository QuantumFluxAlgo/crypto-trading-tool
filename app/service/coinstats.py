import csv
import io
import logging
from datetime import datetime

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud.crud import upsert_coin, upsert_portfolio, store_transaction

logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
async def fetch_portfolio() -> dict:
    """Fetch portfolio data from the CoinStats API."""
    url = f"{settings.coinstats_url}/portfolio"
    headers = {"X-API-KEY": settings.coinstats_api_key}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()


def parse_csv(csv_text: str) -> list[dict]:
    """Parse a CoinStats CSV export and return rows."""
    reader = csv.DictReader(io.StringIO(csv_text))
    required = {"timestamp", "symbol", "amount", "type", "price"}
    rows: list[dict] = []
    for row in reader:
        if not required.issubset(row):
            raise ValueError("Missing required columns")
        rows.append({
            "timestamp": row["timestamp"],
            "symbol": row["symbol"],
            "amount": row["amount"],
            "type": row["type"],
            "price": row["price"],
            "fee": row.get("fee", "0"),
        })
    return rows


def ingest_portfolio_api(db: Session, data: dict) -> None:
    """Create Portfolio entries from API JSON."""
    now = datetime.utcnow()
    for entry in data.get("portfolio", []):
        coin = upsert_coin(
            db,
            symbol=entry["symbol"].lower(),
            name=entry.get("name", entry["symbol"]),
            source="coinstats",
            last_updated=now,
        )
        upsert_portfolio(
            db,
            coin_id=coin.id,
            quantity=float(entry.get("amount", 0)),
            timestamp=now,
            source="coinstats",
        )


def ingest_csv_transactions(db: Session, csv_text: str) -> None:
    """Store Transaction rows from a CSV export."""
    rows = parse_csv(csv_text)
    for r in rows:
        ts = datetime.fromisoformat(r["timestamp"])
        coin = upsert_coin(
            db,
            symbol=r["symbol"].lower(),
            name=r["symbol"],
            source="coinstats",
            last_updated=ts,
        )
        store_transaction(
            db,
            coin_id=coin.id,
            timestamp=ts,
            amount=float(r["amount"]),
            tx_type=r["type"],
            price_usd=float(r["price"]),
            fee_usd=float(r.get("fee", 0) or 0),
            source="coinstats",
        )
