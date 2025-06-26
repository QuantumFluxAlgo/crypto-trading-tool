import httpx
import pytest

from app.service.coingecko import fetch_market
from app.service.cmc import fetch_listings
from app.service.lunarcrush import fetch_sentiment
import tenacity.asyncio as ta

class MockClient:
    def __init__(self, responses):
        self.responses = responses
        self.calls = 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def get(self, *args, **kwargs):
        self.calls += 1
        resp = self.responses[self.calls - 1]
        if isinstance(resp, Exception):
            raise resp
        return resp

class FakeResponse:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self.data


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    original = ta._portable_async_sleep
    async def _sleep(_):
        return None
    monkeypatch.setattr(ta, "_portable_async_sleep", _sleep)
    yield
    monkeypatch.setattr(ta, "_portable_async_sleep", original)

@pytest.mark.asyncio
async def test_fetch_market_retries(monkeypatch):
    responses = [httpx.RequestError('fail'), httpx.RequestError('fail'), FakeResponse([{'id':'btc'}])]
    client = MockClient(responses)
    monkeypatch.setattr(httpx, 'AsyncClient', lambda: client)
    result = await fetch_market(['bitcoin'])
    assert result == [{'id':'btc'}]
    assert client.calls == 3

@pytest.mark.asyncio
async def test_fetch_listings_failure(monkeypatch):
    responses = [httpx.RequestError('boom')] * 3
    client = MockClient(responses)
    monkeypatch.setattr(httpx, 'AsyncClient', lambda: client)
    with pytest.raises(httpx.RequestError):
        await fetch_listings()
    assert client.calls == 3

@pytest.mark.asyncio
async def test_fetch_sentiment_partial_retry(monkeypatch):
    responses = [httpx.RequestError('fail'), FakeResponse({'data': []})]
    client = MockClient(responses)
    monkeypatch.setattr(httpx, 'AsyncClient', lambda: client)
    result = await fetch_sentiment('BTC')
    assert result == {'data': []}
    assert client.calls == 2
