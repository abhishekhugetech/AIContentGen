from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os

api_key_header = APIKeyHeader(name="x-api-key")

def check_x_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == os.getenv("APP_API_KEY"):
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )
