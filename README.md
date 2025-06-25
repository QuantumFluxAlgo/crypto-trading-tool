# Crypto Data API

A modular, extensible FastAPI service that pulls cryptocurrency market data and sentiment metrics from CoinGecko, CoinMarketCap, and LunarCrush. Data is stored in PostgreSQL via SQLAlchemy, with scheduled pulls via APScheduler, fully tested with pytest, and CI/CD powered by GitHub Actions.

---

## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Setup & Configuration](#setup--configuration)
4. [Installation](#installation)
5. [Running Locally](#running-locally)
6. [API Endpoints](#api-endpoints)
7. [Database Schema](#database-schema)
8. [Testing](#testing)
9. [CI/CD](#cicd)

---

## Features

- **Data Sources**: Pulls general market data, structured quotes, and social sentiment.
- **Database**: PostgreSQL backend with Alembic migrations.
- **API**: FastAPI-driven REST endpoints.
- **Scheduler**: APScheduler for periodic pulls respecting free tiers.
- **Testing**: Pytest with in-memory DB for fast, isolated tests.
- **CI/CD**: GitHub Actions for automated testing and migrations validation.

---

## Prerequisites

- Python 3.10 or 3.11
- Homebrew (macOS) or equivalent package manager
- Git & GitHub account with SSH key configured

---

## Setup & Configuration

1. **Clone the repo**:
   ```bash
   git clone git@github.com:QuantumFluxAlgo/crypto-trading-tool.git
   cd crypto-trading-tool
   ```
2. **Environment variables**:
   - Copy `.env.example` → `.env` and fill in:
     ```dotenv
     DATABASE_URL=postgresql://<user>:<pw>@<host>:5432/crypto_db
     COINGECKO_URL=https://api.coingecko.com/api/v3
     COINMARKETCAP_KEY=<your_cmc_key>
     LUNARCRUSH_KEY=<your_lunarcrush_key>
     ```
3. **GitHub Secrets** (for CI): prefix secrets with `SeanKey_` in your repo settings.

---

## Installation

```bash
# Create and activate virtualenv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
git pull origin main
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Running Locally

```bash
# Apply database migrations
alembic upgrade head

# Start the service (scheduler + API)
python -m app.main
# or via Uvicorn:
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for the OpenAPI UI.

---

## API Endpoints

- `GET /api/v1/coins` — List all tracked coins:
  ```json
  [
    {
      "id": 1,
      "symbol": "btc",
      "name": "Bitcoin",
      "source": "coingecko",
      "last_updated": "2025-06-10T12:00:00Z"
    },
    ...
  ]
  ```

---

## Database Schema

- **coins**: `id, symbol, name, source, last_updated`
- **market_data**: `id, coin_id, timestamp, price_usd, market_cap, volume_24h, open_24h, high_24h, low_24h, percent_change_24h, source`
- **sentiment_data**: `id, coin_id, timestamp, galaxy_score, alt_rank, tweet_volume, social_score`

---

## Testing

```bash
# In a new shell
env . .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH="$PWD"
export DATABASE_URL="sqlite:///:memory:"
export COINGECKO_URL="https://api.coingecko.com/api/v3"
export COINMARKETCAP_KEY="dummy"
export LUNARCRUSH_KEY="dummy"
pytest --maxfail=1 -q
```

---

## CI/CD (GitHub Actions)

Workflow path: `.github/workflows/ci.yml`
- **on**: pushes and PRs to `main`
- **jobs**:
  - Checkout, set up Python
  - Install deps
  - Alembic migrations check
  - Run tests across Python 3.10 & 3.11

---

_For contributions, open an issue or submit a pull request._
```

