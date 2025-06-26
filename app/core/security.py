from fastapi import Header, HTTPException, status
from app.core.config import settings

async def api_key_auth(x_api_key: str | None = Header(None)):
    if x_api_key is None or x_api_key not in settings.api_keys_list:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
