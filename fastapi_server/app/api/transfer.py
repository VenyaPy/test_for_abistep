from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import verify_api_key
from ..models import TransferRequest
from ..services.transfer import transfer

router = APIRouter()


@router.post("/transfer", dependencies=[Depends(verify_api_key)])
def transfer_endpoint(payload: TransferRequest) -> dict:
    try:
        transfer(payload.from_user_id, payload.to_user_id, payload.amount)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return {"status": "success"}
