# app/services/coingecko.py
import httpx
from app.core.config import settings

async def fetch_market(coins: list[str]):
    url = f"{settings.coingecko_url}/coins/markets"
    params = {"vs_currency": "usd", "ids": ",".join(coins)}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
