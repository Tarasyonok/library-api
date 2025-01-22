import asyncio
import csv
import ast
from datetime import datetime

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import insert, event, DDL

from app.config import settings
from app.main import app as fastapi_app
from app.mock_data.load_mock_data import load_mock_data
from app.database import Base, async_session_maker, engine

from app.authors.models import Author, AuthorBook
from app.books.models import Book
from app.users.models import User, UserBook
from app.lendings.models import Lending


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    print("********************************\n" * 10)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    event.listen(
        Author.__table__,
        "after_create",
        DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 1001;")
    )

    def open_mock_json(model: str):
        with open(f"app/mock_data/mock_{model}.csv", encoding="utf-8") as file:
            reader = csv.reader(file, quotechar='"', delimiter=',')
            fieldnames = next(reader)
            data = []
            for row in reader:
                row[0] = int(row[0])
                data.append(dict(zip(fieldnames, row)))
            print("!" * 100, data, "!" * 100)
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
        book["amount"] = int(book["amount"])
        book["genres"] = ast.literal_eval(book["genres"])

    for author_book in authors_books:
        author_book["author_id"] = int(author_book["author_id"])
        author_book["book_id"] = int(author_book["book_id"])

    for user_book in users_books:
        user_book["user_id"] = int(user_book["user_id"])
        user_book["book_id"] = int(user_book["book_id"])

    for lending in lendings:
        lending["lend_time"] = datetime.strptime(lending["lend_time"], "%Y-%m-%d")
        lending["return_time"] = datetime.strptime(lending["return_time"], "%Y-%m-%d")
        lending["user_id"] = int(lending["user_id"])
        lending["book_id"] = int(lending["book_id"])

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


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(
            transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    async with AsyncClient(
            transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        await ac.post("/auth/login", json={
            "email": "tester@test.com",
            "password": "tester",
        })
        assert ac.cookies["library_access_token"]
        yield ac


@pytest.fixture(scope="session")
async def authenticated_admin_ac():
    async with AsyncClient(
            transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        await ac.post("/auth/login", json={
            "email": "admin@test.com",
            "password": "admin",
        })
        assert ac.cookies["library_access_token"]
        yield ac
