from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.entity.models import User


async def get_upcoming_birthdays(db: AsyncSession):
    today = datetime.today().date()
    in_7_days = today + timedelta(days=7)
    result = await db.execute(select(User))
    users = result.scalars().all()
    upcoming = []
    for user in users:
        if not user.birthday:
            continue
        birthday = user.birthday
        bday_this_year = birthday.replace(year=today.year)

        if bday_this_year < today:
            bday_this_year = bday_this_year.replace(year=today.year + 1)

        if today <= bday_this_year <= in_7_days:
            upcoming.append(user)

    return upcoming
