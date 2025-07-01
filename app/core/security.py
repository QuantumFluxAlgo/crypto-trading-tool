from fastapi import Header, HTTPException, status
from app.core.config import settings
import pyotp

async def api_key_auth(x_api_key: str | None = Header(None)):
    if x_api_key is None or x_api_key not in settings.api_keys_list:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

async def api_key_totp_auth(
    x_api_key: str | None = Header(None), x_totp: str | None = Header(None)
):
    if x_api_key is None or x_api_key not in settings.api_keys_list:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    if x_totp is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing TOTP",
        )
    totp = pyotp.TOTP(settings.totp_secret)
    if not totp.verify(x_totp, valid_window=1):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid TOTP",
        )
