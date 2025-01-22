from httpx import AsyncClient


async def test_lend_not_authenticated(ac: AsyncClient):
    response = await ac.post(f"/lendings/lend_book", json={
        "lend_time": "2000-01-01",
        "return_time": "2000-02-01",
        "book_id": 1,
    })

    assert response.status_code == 401


async def test_lend_wrong_id(authenticated_ac: AsyncClient):
    response = await authenticated_ac.post(f"/lendings/lend_book", json={
        "lend_time": "2000-01-01",
        "return_time": "2000-02-01",
        "book_id": 999,
    })

    assert response.status_code == 404


async def test_lend_wrong_dates(authenticated_ac: AsyncClient):
    response = await authenticated_ac.post(f"/lendings/lend_book", json={
        "lend_time": "2000-02-01",
        "return_time": "2000-01-01",
        "book_id": 1,
    })

    assert response.status_code == 400
