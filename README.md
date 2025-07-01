# Crypto Trading Tool

This project provides a minimal FastAPI service that collects cryptocurrency market data and sentiment metrics. Data is periodically pulled from public APIs (CoinGecko, CoinMarketCap and LunarCrush) and persisted to a database. The codebase is intentionally small and fully tested so it can be used as a starting point for building automated trading strategies.

---

## Table of Contents
1. [Features](#features)
2. [Requirements](#requirements)
3. [Setup](#setup)
4. [Installation](#installation)
5. [Running the Service](#running-the-service)
6. [API Reference](#api-reference)
7. [Database Schema](#database-schema)
8. [Running Tests](#running-tests)
9. [Continuous Integration](#continuous-integration)

---

## Features
- Collects coin prices and social sentiment.
- Stores information in a PostgreSQL database (or SQLite for tests).
- Exposes REST endpoints via FastAPI.
- Uses APScheduler to run data collection jobs on a schedule.
- Includes a small test suite run by `pytest`.

## Requirements
- Python 3.10 or higher
- Git
- PostgreSQL (or another SQL database)

## Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/QuantumFluxAlgo/crypto-trading-tool.git
   cd crypto-trading-tool
   ```
2. **Environment variables**
   Copy `.env.example` to `.env` and fill in your keys and database URL:
   ```dotenv
   DATABASE_URL=postgresql://user:password@localhost:5432/crypto_db
   COINGECKO_URL=https://api.coingecko.com/api/v3
   COINMARKETCAP_KEY=<your_cmc_key>
   LUNARCRUSH_KEY=<your_lunarcrush_key>
   API_KEYS=your_public_key
   REDIS_URL=redis://localhost:6379/0
   ```

## Installation
It is recommended to use a virtual environment.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Service
1. Apply database migrations:
   ```bash
   alembic upgrade head
   ```
2. Start the scheduler and API:
   ```bash
   python -m app.main
   # or
   uvicorn app.main:app --reload
   ```
3. Open your browser to `http://127.0.0.1:8000/docs` to explore the API.

## Web Dashboard
The project ships with a lightweight dashboard for viewing portfolios.

1. Ensure the `TOTP_SECRET` and `API_KEYS` variables are set in your `.env` file.
2. Run the application with `uvicorn app.main:app --reload` as above.
3. Navigate to `http://127.0.0.1:8000/web/portfolios` and supply both `X-API-Key`
   and `X-TOTP` headers. The TOTP value should be generated from `TOTP_SECRET`
   using any authenticator app.

## API Reference
All requests must include an `X-API-Key` header. The service currently exposes a single endpoint that is limited to 20 requests per minute per key:
- `GET /api/v1/coins` – list all coins stored in the database.

The API will expand as trading strategies and exchange integrations are added.
---

## Database Schema

- **coins**: `id, symbol, name, source, last_updated`
- **market_data**: `id, coin_id, timestamp, price_usd, market_cap, volume_24h, open_24h, high_24h, low_24h, percent_change_24h, source`
- **sentiment_data**: `id, coin_id, timestamp, galaxy_score, alt_rank, tweet_volume, social_score`
- **portfolios**: `id, name`
- **portfolio_assets**: `id, portfolio_id, coin_id, quantity`

See `app/models/models.py` for the exact column definitions.

## Running Tests
Tests use an in-memory SQLite database. Activate your virtual environment and run:
```bash
export PYTHONPATH="$PWD"
export DATABASE_URL="sqlite:///:memory:"
export COINGECKO_URL="https://api.coingecko.com/api/v3"
export COINMARKETCAP_KEY="dummy"
export LUNARCRUSH_KEY="dummy"
pytest -q
```

## Continuous Integration
GitHub Actions runs the test suite and validates migrations on every push or pull request. The workflow file lives in `.github/workflows/ci.yml`.

---
This project is a foundation for a future trading bot. Data collection is implemented; strategy logic and exchange execution will be added later.
