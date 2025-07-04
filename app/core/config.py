# app/core/config.py
from dotenv import load_dotenv
load_dotenv()   # pip install python-dotenv

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    coingecko_url: str
    coinmarketcap_key: str
    lunarcrush_key: str
    api_keys: str = "localtestkey"
    redis_url: str = "redis://localhost:6379/0"

    @property
    def api_keys_list(self) -> list[str]:
        return [k.strip() for k in self.api_keys.split(',') if k.strip()]
        
    class Config:
        env_file = ".env"

settings = Settings()

