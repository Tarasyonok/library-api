from sqlalchemy import insert, select, delete

from app.books.dao import BookDAO
from app.books.models import Book
from app.database import async_session_maker
from app.exceptions import BookNotFoundException, UserDoesntExistException, ReturnTimeBeforeLendTimeException, \
    BookAlreadyLentException, NoBooksLeftException, FiveBooksLentException, UserDoesntHaveThisBookException
from app.lendings.models import Lending
from app.users.dao import UserDAO
from app.users.models import User


class LendingDAO:
    @classmethod
    async def find_by_id(cls, id):
        async with async_session_maker() as session:
            query = select(Lending.__table__.columns).filter_by(id=id)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(Lending.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def lend_book(cls, book_id, user_id, lend_time, return_time):
        async with async_session_maker() as session:
            if return_time <= lend_time:
                raise ReturnTimeBeforeLendTimeException
            book = await BookDAO.find_one_or_none(id=book_id)
            if not book:
                raise BookNotFoundException
            user = await UserDAO.find_one_or_none(id=user_id)
            if not user:
                raise UserDoesntExistException
            for b in user.books:
                if b.id == book.id:
                    raise BookAlreadyLentException

            if book.amount <= 0:
                raise NoBooksLeftException
            if len(user.books) >= 5:
                raise FiveBooksLentException

            book = await session.get(Book, book_id)
            user = await session.get(User, user_id)

            user.books = [book]
            await session.commit()

            query = insert(Lending).values(book_id=book_id, user_id=user_id, lend_time=lend_time,
                                           return_time=return_time)
            await session.execute(query)
            await session.commit()
            return

    @classmethod
    async def return_book(cls, book_id, user_id):
        async with async_session_maker() as session:
            book = await BookDAO.find_one_or_none(id=book_id)
            if not book:
                raise BookNotFoundException
            user = await UserDAO.find_one_or_none(id=user_id)
            if not user:
                raise UserDoesntExistException
            for b in user.books:
                if b.id == book.id:
                    user = await session.get(User, user_id)
                    book = await session.get(Book, book_id)
                    user.books.remove(book)
                    await session.commit()
                    break
            else:
                raise UserDoesntHaveThisBookException

            query = delete(Lending).filter_by(book_id=book_id, user_id=user_id)
            await session.execute(query)
            await session.commit()
            return

    @classmethod
    async def return_book_via_id(cls, id):
        async with async_session_maker() as session:
            lending = await session.get(Lending, id)
            user = await UserDAO.find_one_or_none(id=lending.user_id)
            book = await UserDAO.find_one_or_none(id=lending.book_id)
            try:
                user.books.remove(book)
                await session.commit()
            except ValueError:
                ...

            query = delete(Lending).filter_by(id=lending.id)
            await session.execute(query)
            await session.commit()
            return
