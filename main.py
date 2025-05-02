from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, status, Query
from sqlalchemy import text, or_
from sqlalchemy.orm import Session
from db import get_db
from models import User
from schemas import UserResponse, UserShema

app = FastAPI()


@app.get("/api/users", response_model=list[UserResponse], tags=["users"])
async def get_users(
        name: Optional[str] = Query(None, description="Filter by name"),
        surname: Optional[str] = Query(None, description="Filter by surname"),
        email: Optional[str] = Query(None, description="Filter by email"),
        db: Session = Depends(get_db)
):
    query = db.query(User)
    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))
    if surname:
        query = query.filter(User.surname.ilike(f"%{surname}%"))
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    users = query.all()
    return users


@app.post("/api/users", response_model=UserResponse, tags=["users"])
async def create_user(body: UserShema, db: Session = Depends(get_db)):
    is_exist = db.query(User).filter(
        or_(User.email == body.email, User.phone == body.phone)
    ).first()
    if is_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is exists")
    user = User(**body.model_dump())
    db.add(user)
    db.commit()
    return user


@app.get("/api/users/{user_id}", response_model=UserResponse, tags=["users"])
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.put("/api/users/{user_id}", response_model=UserResponse, tags=["users"])
async def update_user(body: UserShema, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.name = body.name
    user.surname = body.surname
    user.email = body.email
    user.phone = body.phone
    if body.birthday is not None:
        user.birthday = body.birthday
    if body.additional_data is not None:
        user.additional_data = body.additional_data
    db.commit()
    return user


@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/api/users/upcoming_birthdays", response_model=list[UserResponse], tags=["users"])
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    today = datetime.today()
    in_7_days = today + timedelta(days=7)
    users = db.query(User).all()
    upcoming = []
    for user in users:
        if not user.birthday:
            continue
        bday_this_year = user.birthday.replace(year=today.year)
        if bday_this_year < today:
            bday_this_year = bday_this_year.replace(year=today.year + 1)
        if today <= bday_this_year <= in_7_days:
            upcoming.append(user)
    return upcoming


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise Exception()
        return {"message": "Welcome to FastAPI!"}
    except Exception:
        raise HTTPException(status_code=500, detail="Database is not configured.")
