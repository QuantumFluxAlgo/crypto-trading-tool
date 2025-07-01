from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.crud.crud import (
    get_all_portfolios,
    get_portfolio,
    get_portfolio_assets,
)
from app.core.security import api_key_totp_auth

templates = Jinja2Templates(directory="app/web/templates")
router = APIRouter(prefix="/web", dependencies=[Depends(api_key_totp_auth)])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/portfolios")
async def list_portfolios(request: Request, db: Session = Depends(get_db)):
    portfolios = get_all_portfolios(db)
    return templates.TemplateResponse(
        "portfolio_list.html", {"request": request, "portfolios": portfolios}
    )


@router.get("/portfolios/{portfolio_id}")
async def portfolio_detail(portfolio_id: int, request: Request, db: Session = Depends(get_db)):
    portfolio = get_portfolio(db, portfolio_id)
    assets = get_portfolio_assets(db, portfolio_id)
    return templates.TemplateResponse(
        "portfolio_detail.html",
        {"request": request, "portfolio": portfolio, "assets": assets},
    )
