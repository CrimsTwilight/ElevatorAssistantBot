from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.testing.suite.test_reflection import users

from app.database.models import async_session, User


async def add_user(tg_id, full_name, username):
    date = datetime.today()

    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, full_name=full_name,
                             username=username, date=date.strftime("%d.%m.%Y %H:%M:%S")))
            await session.commit()


async def show_number_of_users():
    async with async_session() as session:
        user_count = await session.scalar(select(func.count(User.id)))
        return user_count


async def get_all_users():
    async with async_session() as session:
        all_users = (await session.scalars(select(User))).all()
        return all_users
