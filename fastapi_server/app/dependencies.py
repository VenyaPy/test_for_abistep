import os
from fastapi import Header, HTTPException, status


def verify_api_key(x_api_key: str | None = Header(None)) -> None:
    api_key = os.getenv("API_KEY")
    if api_key is None or x_api_key != api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
