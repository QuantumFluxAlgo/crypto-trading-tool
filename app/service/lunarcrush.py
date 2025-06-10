import httpx
from app.core.config import settings

async def fetch_sentiment(symbol: str):
    url = "https://api.lunarcrush.com/v2"
    params = {"data": "assets", "symbol": symbol, "key": settings.lunarcrush_key}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
