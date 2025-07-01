import os
import pytest
import fakeredis
from fastapi_limiter import FastAPILimiter

# Ensure environment variables are present before modules import Settings
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("COINGECKO_URL", "https://api.coingecko.com/api/v3")
os.environ.setdefault("COINMARKETCAP_KEY", "dummy")
os.environ.setdefault("LUNARCRUSH_KEY", "dummy")
os.environ.setdefault("COINSTATS_API_KEY", "dummy")
os.environ.setdefault("COINSTATS_URL", "https://api.coinstats.app")
os.environ.setdefault("API_KEYS", "testkey")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("TESTING", "1")

@pytest.fixture(scope="session", autouse=True)
def env_settings():
    mp = pytest.MonkeyPatch()
    mp.setenv("DATABASE_URL", "sqlite:///:memory:")
    mp.setenv("COINGECKO_URL", "https://api.coingecko.com/api/v3")
    mp.setenv("COINMARKETCAP_KEY", "dummy")
    mp.setenv("LUNARCRUSH_KEY", "dummy")
    mp.setenv("COINSTATS_API_KEY", "dummy")
    mp.setenv("COINSTATS_URL", "https://api.coinstats.app")
    mp.setenv("API_KEYS", "testkey")
    mp.setenv("REDIS_URL", "redis://localhost:6379/0")
    mp.setenv("TESTING", "1")
    mp.setenv("REDIS_URL", "redis://localhost:6379/0")
    yield
    mp.undo()


@pytest.fixture(autouse=True)
def fake_redis(monkeypatch):
    # Use actual Redis server if available; fall back to fakeredis
    try:
        import redis
        redis.Redis.from_url("redis://localhost:6379/0").ping()
    except Exception:
        monkeypatch.setattr('redis.Redis.from_url', lambda *a, **kw: fakeredis.FakeRedis())
        monkeypatch.setattr('redis.asyncio.Redis.from_url', lambda *a, **kw: fakeredis.FakeRedis())
    yield

