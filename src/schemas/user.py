from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional


class UserShema(BaseModel):
    name: str = Field(..., max_length=150, min_length=1)
    surname: str = Field(..., min_length=1, max_length=150)
    email: EmailStr
    phone: str = Field(..., min_length=5, max_length=20)
    birthday: Optional[date] = None
    additional_data: Optional[str] = None


class UserResponse(UserShema):
    id: int = Field(..., gt=0)

    class Config:
        orm_mode = True
