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
async def fetch_listings():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"X-CMC_PRO_API_KEY": settings.coinmarketcap_key}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

