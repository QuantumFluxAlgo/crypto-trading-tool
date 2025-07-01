import typer
from app.db.session import SessionLocal
from app.crud import crud

app = typer.Typer(help="Portfolio management commands")


@app.command()
def live():
    """Display the total current value of the portfolio."""
    db = SessionLocal()
    total = 0.0
    for pos in crud.get_portfolio_positions(db):
        md = crud.get_latest_market_price(db, pos.coin_id)
        if md:
            total += float(md.price_usd) * float(pos.quantity)
    db.close()
    typer.echo(f"Live portfolio value: ${total:,.2f}")


@app.command()
def gains():
    """Show unrealized and realized gains for each asset and exchange."""
    db = SessionLocal()
    for pos in crud.get_portfolio_positions(db):
        md = crud.get_latest_market_price(db, pos.coin_id)
        if not md:
            continue
        price = float(md.price_usd)
        unrealized = (price - float(pos.avg_price)) * float(pos.quantity)
        typer.echo(
            f"{pos.coin.symbol.upper()} on {pos.exchange}: "
            f"unrealized {unrealized:.2f}, realized {float(pos.realized_pnl):.2f}"
        )
    db.close()


@app.command()
def summary():
    """Show summaries at the exchange and asset level."""
    db = SessionLocal()
    exch: dict[str, float] = {}
    assets: dict[str, dict[str, float]] = {}
    for pos in crud.get_portfolio_positions(db):
        md = crud.get_latest_market_price(db, pos.coin_id)
        price = float(md.price_usd) if md else 0.0
        value = price * float(pos.quantity)
        exch[pos.exchange] = exch.get(pos.exchange, 0.0) + value
        info = assets.setdefault(pos.coin.symbol, {"qty": 0.0, "value": 0.0})
        info["qty"] += float(pos.quantity)
        info["value"] += value
    db.close()

    typer.echo("Exchange Summary:")
    for name, val in exch.items():
        typer.echo(f"  {name}: ${val:,.2f}")
    typer.echo("Asset Summary:")
    for sym, info in assets.items():
        typer.echo(f"  {sym.upper()}: qty {info['qty']}, value ${info['value']:,.2f}")


if __name__ == "__main__":
    app()
