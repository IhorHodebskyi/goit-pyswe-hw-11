from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import birthdays as repository_birthdays
from src.schemas.user import UserResponse, UserShema

router = APIRouter(prefix="/birthdays", tags=["birthdays"])

@router.get("/upcoming_birthdays", response_model=list[UserResponse])
async def get_upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    users = await repository_birthdays.get_upcoming_birthdays(db=db)
    return users

