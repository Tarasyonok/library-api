import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("id,status_code", [
    (1, 200),
    (2, 200),
    (999, 404),
])
async def test_get_by_id(id, status_code, ac: AsyncClient):
    response = await ac.get(f"/books/by_id/{id}")
    assert response.status_code == status_code

    if status_code == 200:
        book = response.json()
        assert book
        assert book["id"] == id


async def test_get_all(ac: AsyncClient):
    response = await ac.get("/books")
    assert response.status_code == 200

    assert isinstance(response.json(), list)


async def test_add_not_authenticated(ac: AsyncClient):
    response = await ac.post(f"/books", json={
        "name": "test",
        "description": "test",
        "pub_date": "2000-01-01",
        "genres": ["test"],
        "authors": [],
        "amount": 0,
    })

    assert response.status_code == 401


async def test_add_not_admin(authenticated_ac: AsyncClient):
    response = await authenticated_ac.post(f"/books", json={
        "name": "test",
        "description": "test",
        "pub_date": "2000-01-01",
        "genres": ["test"],
        "authors": [],
        "amount": 0,
    })

    assert response.status_code == 403


async def test_add_incorrect(authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.post(f"/books", json={
        "name": None,
        "description": "test",
        "pub_date": "2000-01-01",
        "genres": ["test"],
        "authors": [],
        "amount": 0,
    })

    assert response.status_code == 422


async def test_add_correct_and_delete(authenticated_admin_ac: AsyncClient):
    response = await authenticated_admin_ac.post(f"/books", json={
        "name": "test",
        "description": "test",
        "pub_date": "2000-01-01",
        "genres": ["test"],
        "authors": [],
        "amount": 0,
    })

    assert response.status_code == 201

    response = await authenticated_admin_ac.delete(f"/books/101")

    assert response.status_code == 200
