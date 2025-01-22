from sqlalchemy import insert, delete, select, update
from sqlalchemy.orm import joinedload

from app.books.models import Book
from app.database import async_session_maker

from app.users.models import User
from app.dao.base import BaseDAO


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(User.books)).filter_by(**filter_by)
            result = await session.execute(query)
            user = result.unique().first()
            if user:
                user = user[0]
            return user

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(User.books)).filter_by(**filter_by)
            result = await session.execute(query)
            return result.unique().scalars().all()

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            user = result.mappings().one_or_none()
            if not user:
                return
            user_id = user.id
            user = await session.get(User, user_id)
            user.books = []
            await session.commit()
            query = delete(cls.model).filter_by(id=user_id)
            await session.execute(query)
            await session.commit()
            return user_id
