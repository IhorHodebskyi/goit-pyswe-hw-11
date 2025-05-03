from fastapi import Depends
from sqlalchemy import select, or_, cast, String
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db

from src.entity.models import User
from src.schemas.user import  UserShema


async def get_users(limit: int, offset: int, query: str | None,
                    db: AsyncSession = Depends(get_db)):
    stmt = select(User).offset(offset).limit(limit)
    if query:
        search = f"%{query.lower()}%"
        stmt = stmt.where(or_(
            User.name.ilike(search),
            User.email.ilike(search),
            User.phone.ilike(search),
            cast(User.birthday, String).like(search),
            User.additional_data.ilike(search)
        ))
    result = await db.execute(stmt)
    return result.scalars().unique().all()


async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def create_user(user: UserShema, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(or_(User.email == user.email, User.phone == user.phone))
    result = await db.execute(stmt)
    user_in_db = result.scalars().unique().first()
    if user_in_db:
        return None
    new_user = User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_user(user_id: int, user: UserShema, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user_in_db = result.scalars().unique().first()
    if not user_in_db:
        return None
    user_in_db.name = user.name
    user_in_db.surname = user.surname
    user_in_db.email = user.email
    user_in_db.phone = user.phone
    if user.birthday:
        user_in_db.birthday = user.birthday
    if user_in_db.birthday:
        user_in_db.additional_data = user.additional_data
    await db.commit()
    await db.refresh(user_in_db)
    return user_in_db


async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user_in_db = result.scalars().unique().first()
    if not user_in_db:
        return None
    await db.delete(user_in_db)
    await db.commit()
    return user_in_db



