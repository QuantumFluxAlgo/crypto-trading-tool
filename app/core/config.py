# app/core/config.py
from dotenv import load_dotenv
load_dotenv()   # pip install python-dotenv

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    coingecko_url: str
    coinmarketcap_key: str
    lunarcrush_key: str

    class Config:
        env_file = ".env"

settings = Settings()

