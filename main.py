from fastapi import FastAPI, HTTPException, Depends, status, Query
from sqlalchemy import text, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.middleware.middleware import CustomMiddleware
from src.routes import users, birthdays

app = FastAPI()

app.add_middleware(CustomMiddleware)

app.include_router(users.router, prefix="/api", tags=["users"])

app.include_router(birthdays.router, prefix="/api", tags=["birthdays"])


@app.get("/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        result = await (db.execute(text("SELECT 1")))
        result = result.fetchone()
        if result is None:
            raise Exception()
        return {"message": "Welcome to FastAPI!"}

    except Exception:
        raise HTTPException(status_code=500, detail="Database is not configured.")
