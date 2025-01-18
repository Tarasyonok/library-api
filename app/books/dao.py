from typing import List

from sqlalchemy import insert, delete, select, update
from sqlalchemy.orm import joinedload

from app.authors.models import Author
from app.books.schemas import BookFilter
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
        data['genres'] = [g.lower() for g in data['genres']]

        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(query)
            book_id = int(result.mappings().first()['id'])
            await session.commit()

            book = await session.get(Book, book_id)

            for author_id in authors_ids:
                author = await session.get(Author, author_id)
                book.authors.append(author)

            await session.commit()
            return book.id

    @classmethod
    async def update(cls, id, **data):
        authors_ids = data['authors']
        del data['authors']
        data['genres'] = [g.lower() for g in data['genres']]

        async with async_session_maker() as session:
            book = await session.get(Book, id)
            query = update(Book).where(Book.id == id).values(**data)
            await session.execute(query)
            await session.commit()

            book.authors = []
            for author_id in authors_ids:
                author = await session.get(Author, author_id)
                book.authors.append(author)

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

    @classmethod
    async def filter(cls, book_filter: BookFilter, page: int, size: int):
        async with async_session_maker() as session:
            genres = list(map(str.strip, map(str.lower, book_filter.genres__in)))
            delattr(book_filter, "genres__in")
            # print(genres)
            # print(book_filter.filtering_fields)
            offset = page * size
            limit = size

            query = select(Book).options(joinedload(Book.authors)).options(joinedload(Book.users))
            if genres:
                query = query.filter(Book.genres.comparator.contains(genres))
            query = query.limit(limit).offset(offset)
            filter_query = book_filter.filter(query)
            result = await session.execute(filter_query)
            return result.unique().scalars().all()
