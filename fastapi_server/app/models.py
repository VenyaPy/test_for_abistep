from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    balance: float = Field(..., ge=0)


class User(UserCreate):
    id: int


class TransferRequest(BaseModel):
    from_user_id: int
    to_user_id: int
    amount: float = Field(..., gt=0)
