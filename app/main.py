import asyncio
from datetime import datetime

from fastapi import FastAPI
import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.api.v1.endpoints import router as v1_router
from app.db.session import SessionLocal
from app.crud.crud import upsert_coin, store_market_data, store_sentiment_data
from app.service.coingecko import fetch_market
from app.service.cmc import fetch_listings
from app.service.lunarcrush import fetch_sentiment

app = FastAPI(title="Crypto Data API")
app.include_router(v1_router)

# === Scheduler Configuration ===
scheduler = AsyncIOScheduler()

def job_gecko():
    db = SessionLocal()
    now = datetime.utcnow()
    data = asyncio.run(fetch_market(['bitcoin', 'ethereum']))
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
                open_24h=item.get('open_24h'),
                percent_change_24h=item.get('price_change_percentage_24h'),
                source='coingecko'
            )
    db.close()

def job_cmc():
    db = SessionLocal()
    now = datetime.utcnow()
    resp = asyncio.run(fetch_listings())
    with db.begin():
        for item in resp['data']:
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
                percent_change_1h=item['quote']['USD']['percent_change_1h'],
                percent_change_24h=item['quote']['USD']['percent_change_24h'],
                open_24h=item['quote']['USD'].get('open_24h'),
                high_24h=item['quote']['USD'].get('high_24h'),
                low_24h=item['quote']['USD'].get('low_24h'),
                percent_change_24h=item['quote']['USD'].get('percent_change_24h'),
                source='coinmarketcap'
            )
    db.close()

def job_lunar():
    db = SessionLocal()
    for symbol in ['BTC', 'ETH']:
        resp = asyncio.run(fetch_sentiment(symbol))
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
scheduler.add_job(job_gecko, 'interval', minutes=1)
scheduler.add_job(job_cmc,   'cron',    hour='*/2')
scheduler.add_job(job_lunar, 'cron',    hour='*/6')

# === Entrypoint: start scheduler only when running directly ===
if __name__ == "__main__":
    scheduler.start()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
