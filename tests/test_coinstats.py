import httpx
import pytest
import tenacity.asyncio as ta

from app.service.coinstats import fetch_portfolio, parse_csv

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


def test_parse_csv():
    csv_text = (
        "timestamp,symbol,amount,type,price,fee\n"
        "2024-01-01T00:00:00,btc,0.1,buy,10000,10\n"
        "2024-01-02T00:00:00,eth,1,sell,2000,2\n"
    )
    rows = parse_csv(csv_text)
    assert len(rows) == 2
    assert rows[0]["symbol"] == "btc"
    assert rows[1]["type"] == "sell"


def test_parse_csv_missing_col():
    bad_csv = "symbol,amount\nBTC,1"
    with pytest.raises(ValueError):
        parse_csv(bad_csv)


@pytest.mark.asyncio
async def test_fetch_portfolio_retry(monkeypatch):
    responses = [httpx.RequestError("fail"), FakeResponse({"portfolio": []})]
    client = MockClient(responses)
    monkeypatch.setattr(httpx, "AsyncClient", lambda: client)
    result = await fetch_portfolio()
    assert result == {"portfolio": []}
    assert client.calls == 2
