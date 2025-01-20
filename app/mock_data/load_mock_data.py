import csv
from datetime import datetime

from sqlalchemy import insert

from app.database import Base, async_session_maker, engine

from app.authors.models import Author, AuthorBook
from app.books.models import Book
from app.users.models import User, UserBook
from app.lendings.models import Lending


async def load_mock_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/mock_data/mock_{model}.csv", encoding="utf-8") as file:
            reader = csv.reader(file)
            fieldnames = next(reader)
            data = []
            for row in reader:
                data.append(dict(zip(fieldnames, row)))
            return data

    authors = open_mock_json("authors")
    users = open_mock_json("users")
    books = open_mock_json("books")
    authors_books = open_mock_json("authors_books")
    users_books = open_mock_json("users_books")
    lendings = open_mock_json("lendings")

    for author in authors:
        author["birthday"] = datetime.strptime(author["birthday"], "%Y-%m-%d")

    for book in books:
        book["pub_date"] = datetime.strptime(book["pub_date"], "%Y-%m-%d")

    for lending in lendings:
        lending["lend_time"] = datetime.strptime(lending["lend_time"], "%Y-%m-%d")
        lending["return_time"] = datetime.strptime(lending["return_time"], "%Y-%m-%d")

    async with async_session_maker() as session:
        for Model, values in [
            (Author, authors),
            (User, users),
            (Book, books),
            (AuthorBook, authors_books),
            (UserBook, users_books),
            (Lending, lendings),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


if __name__ == "__main__":
    load_mock_data()