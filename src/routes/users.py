from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import users as repository_users
from src.schemas.user import UserResponse, UserShema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def get_users(limit: int = Query(10), offset: int = Query(0, ge=0), query: str | None = Query(None),
                    db: AsyncSession = Depends(get_db)):
    user = await repository_users.get_users(limit=limit, offset=offset, query=query, db=db)
    return user


#
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await repository_users.get_user_by_id(user_id=user_id, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=UserResponse)
async def create_user(user: UserShema, db: AsyncSession = Depends(get_db)):
    user = await repository_users.create_user(user=user, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User with this email or phone already exists")
    return user


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id: int, user: UserShema, db: AsyncSession = Depends(get_db)):
    user = await repository_users.update_user(user_id=user_id, user=user, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
#
#
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)):
    user = await repository_users.delete_user(user_id=user_id, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="User deleted")



