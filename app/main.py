from datetime import datetime

from fastapi import FastAPI
import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
import os

from app.api.v1.endpoints import router as v1_router
from app.db.session import SessionLocal
from app.crud.crud import upsert_coin, store_market_data, store_sentiment_data
from app.service.coingecko import fetch_market
from app.service.cmc import fetch_listings
from app.service.lunarcrush import fetch_sentiment
from app.core.config import settings
from app.core.coins import TRACKED_COINS
from app.models.models import Coin

app = FastAPI(title="Crypto Data API")
app.include_router(v1_router)

@app.on_event("startup")
async def startup_event():
    redis_client = redis.from_url(
        settings.redis_url, encoding="utf-8", decode_responses=True
    )
    await FastAPILimiter.init(redis_client)

@app.on_event("shutdown")
async def shutdown_event():
    await FastAPILimiter.close()
    
# === Scheduler Configuration ===
scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def start_scheduler():
    if not os.getenv("TESTING") and not scheduler.running:
        scheduler.start()


@app.on_event("shutdown")
async def stop_scheduler():
    if not os.getenv("TESTING") and scheduler.running:
        scheduler.shutdown()

async def job_gecko():
    db = SessionLocal()
    now = datetime.utcnow()
    data = await fetch_market(TRACKED_COINS)
    with db.begin():
        for item in data:
            coin = upsert_coin(
                db,
                symbol=item['symbol'],
                name=item['name'],
                source='coingecko',
                last_updated=now
            )
            store_market_data(
                db,
                coin_id=coin.id,
                timestamp=now,
                price_usd=item['current_price'],
                market_cap=item['market_cap'],
                volume_24h=item['total_volume'],
                high_24h=item['high_24h'],
                low_24h=item['low_24h'],
                price_change_24h=item['price_change_24h'],
                price_change_percentage_24h=item['price_change_percentage_24h'],
                percent_change_1h=None,
                percent_change_24h=item.get('price_change_percentage_24h'),
                open_24h=item.get('open_24h'),
                source='coingecko',
            )
    db.close()

async def job_cmc():
    db = SessionLocal()
    now = datetime.utcnow()
    resp = await fetch_listings()
    with db.begin():
        for item in resp['data']:
            if item.get('slug') not in TRACKED_COINS:
                continue
            coin = upsert_coin(
                db,
                symbol=item['symbol'],
                name=item['name'],
                source='coinmarketcap',
                last_updated=now
            )
            store_market_data(
                db,
                coin_id=coin.id,
                timestamp=now,
                price_usd=item['quote']['USD']['price'],
                market_cap=item['quote']['USD']['market_cap'],
                volume_24h=item['quote']['USD']['volume_24h'],
                high_24h=item['quote']['USD'].get('high_24h'),
                low_24h=item['quote']['USD'].get('low_24h'),
                price_change_24h=item['quote']['USD'].get('price_change_24h'),
                price_change_percentage_24h=item['quote']['USD'].get('percent_change_24h'),
                percent_change_1h=item['quote']['USD'].get('percent_change_1h'),
                percent_change_24h=item['quote']['USD'].get('percent_change_24h'),
                open_24h=item['quote']['USD'].get('open_24h'),
                source='coinmarketcap',
            )
    db.close()

async def job_lunar():
    db = SessionLocal()
    symbols = [c.symbol.upper() for c in db.query(Coin.symbol).all()]
    for symbol in symbols:
        resp = await fetch_sentiment(symbol)
        d = resp['data'][0]
        now = datetime.strptime(
            d['time_series'][0]['time'], '%Y-%m-%dT%H:%M:%SZ'
        )
        with db.begin():
            coin = upsert_coin(
                db,
                symbol=symbol.lower(),
                name=symbol,
                source='lunarcrush',
                last_updated=now
            )
            store_sentiment_data(
                db,
                coin_id=coin.id,
                timestamp=now,
                galaxy_score=d['galaxy_score'],
                alt_rank=d['alt_rank'],
                tweet_volume=d['tweet_volume'],
                social_score=d['social_score']
            )
    db.close()

# Register jobs (do not start here)
scheduler.add_job(job_gecko, 'interval', minutes=1, max_instances=1)
scheduler.add_job(job_cmc,   'cron',    hour='*/2', max_instances=1)
scheduler.add_job(job_lunar, 'cron',    hour='*/6', max_instances=1)

# === Entrypoint: start scheduler only when running directly ===
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
