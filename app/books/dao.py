from sqlalchemy import insert, delete, select, update
from sqlalchemy.orm import joinedload

from app.authors.models import Author
from app.database import async_session_maker

from app.books.models import Book
from app.dao.base import BaseDAO
from app.users.models import User


class BookDAO(BaseDAO):
    model = Book

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(Book.authors)) \
                .options(joinedload(Book.users)).filter_by(**filter_by)
            result = await session.execute(query)
            book = result.unique().first()
            if book:
                book = book[0]
            return book

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(Book.authors)) \
                .options(joinedload(Book.users)).filter_by(**filter_by)
            result = await session.execute(query)
            return result.unique().scalars().all()

    @classmethod
    async def add(cls, **data):
        authors_ids = data['authors']
        del data['authors']

        users_ids = data['users']
        del data['users']

        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(query)
            book_id = int(result.mappings().first()['id'])
            await session.commit()

            book = await session.get(Book, book_id)

            for author_id in authors_ids:
                author = await session.get(Author, author_id)
                book.authors.append(author)

            for user_id in users_ids:
                user = await session.get(User, user_id)
                book.users.append(user)

            await session.commit()
            return book.id

    @classmethod
    async def update(cls, id, **data):
        authors_ids = data['authors']
        del data['authors']

        users_ids = data['users']
        del data['users']

        async with async_session_maker() as session:
            book = await session.get(Book, id)
            query = update(Book).where(Book.id == id).values(**data)
            await session.execute(query)
            await session.commit()

            book.authors = []
            for author_id in authors_ids:
                author = await session.get(Author, author_id)
                book.authors.append(author)

            book.users = []
            for user_id in users_ids:
                user = await session.get(User, user_id)
                book.users.append(user)

            await session.commit()
            return book.id

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            book_id = result.mappings().one_or_none().id
            book = await session.get(Book, book_id)
            book.authors = []
            book.users = []
            await session.commit()
            query = delete(cls.model).filter_by(id=book_id)
            await session.execute(query)
            await session.commit()
            return book.id
