import httpx
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
from app.core.config import settings

logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
async def fetch_sentiment(symbol: str):
    url = "https://api.lunarcrush.com/v2"
    params = {"data": "assets", "symbol": symbol, "key": settings.lunarcrush_key}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

