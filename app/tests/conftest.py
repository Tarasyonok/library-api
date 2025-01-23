import asyncio

import pytest
from httpx import AsyncClient, ASGITransport

from app.config import settings
from app.main import app as fastapi_app
from app.mock_data.load_mock_data import load_mock_data
from app.database import Base, engine



@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await load_mock_data()


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
