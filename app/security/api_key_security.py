from fastapi.security import APIKeyHeader
from fastapi import HTTPException,Security
import secrets

from app.config import MY_API_KEY

api_key_header = APIKeyHeader(name="X-API-Key",auto_error=False)

async def verify_api_key(api_key:str | None = Security(api_key_header)):
    if not api_key or not secrets.compare_digest(MY_API_KEY,api_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key",
        )
