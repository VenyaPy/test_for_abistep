from fastapi import APIRouter, Depends

from ..dependencies import verify_api_key

router = APIRouter()


@router.get("/ping", dependencies=[Depends(verify_api_key)])
def ping() -> dict:
    return {"status": "ok"}
