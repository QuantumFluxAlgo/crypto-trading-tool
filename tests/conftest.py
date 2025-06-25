import os
import pytest

# Ensure environment variables are present before modules import Settings
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("COINGECKO_URL", "https://api.coingecko.com/api/v3")
os.environ.setdefault("COINMARKETCAP_KEY", "dummy")
os.environ.setdefault("LUNARCRUSH_KEY", "dummy")

@pytest.fixture(scope="session", autouse=True)
def env_settings():
    mp = pytest.MonkeyPatch()
    mp.setenv("DATABASE_URL", "sqlite:///:memory:")
    mp.setenv("COINGECKO_URL", "https://api.coingecko.com/api/v3")
    mp.setenv("COINMARKETCAP_KEY", "dummy")
    mp.setenv("LUNARCRUSH_KEY", "dummy")
    yield
    mp.undo()

