from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        query = insert(cls.model).values(**data).returning(cls.model.id)
        async with async_session_maker() as session:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()["id"]

    @classmethod
    async def update(cls, id, **data):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == id).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
