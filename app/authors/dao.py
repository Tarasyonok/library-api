from sqlalchemy import insert, delete, select, update
from sqlalchemy.orm import joinedload

from app.books.models import Book
from app.database import async_session_maker

from app.authors.models import Author
from app.dao.base import BaseDAO


class AuthorDAO(BaseDAO):
    model = Author

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(Author.books)).filter_by(**filter_by)
            result = await session.execute(query)
            author = result.unique().first()
            if author:
                author = author[0]
            return author

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(Author.books)).filter_by(**filter_by)
            result = await session.execute(query)
            return result.unique().scalars().all()

    @classmethod
    async def add(cls, **data):
        books_ids = data['books']
        del data['books']

        query = insert(cls.model).values(**data)
        async with async_session_maker() as session:
            await session.execute(query)
            await session.commit()

            author = await session.get(Author, data['id'])

            for book_id in books_ids:
                book = await session.get(Book, book_id)
                author.books.append(book)

            await session.commit()
            return author.id

    @classmethod
    async def update(cls, id, **data):

        # async with async_session_maker() as session:
        #     cls.model.query.get(id).update(**data)
        #     await session.commit()

        async with async_session_maker() as session:
            books_ids = data['books']
            del data['books']

            author = await session.get(Author, id)
            query = update(Author).where(Author.id == id).values(**data)
            await session.execute(query)
            await session.commit()

            author.books = []
            for book_id in books_ids:
                book = await session.get(Book, book_id)
                author.books.append(book)

            await session.commit()
            return author.id

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            author_id = result.mappings().one_or_none().id
            author = await session.get(Author, author_id)
            author.books = []
            await session.commit()
            query = delete(cls.model).filter_by(id=author_id)
            await session.execute(query)
            await session.commit()
            return author.id
