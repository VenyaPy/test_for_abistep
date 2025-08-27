from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import verify_api_key
from ..models import User, UserCreate
from ..services.users import create_user, list_users

router = APIRouter(prefix="/users")


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_api_key)])
def create_user_endpoint(user: UserCreate) -> User:
    try:
        return create_user(user)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("", response_model=list[User], dependencies=[Depends(verify_api_key)])
def list_users_endpoint() -> list[User]:
    return list_users()
