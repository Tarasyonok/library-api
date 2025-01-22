from httpx import AsyncClient


async def test_lend(authenticated_ac: AsyncClient):
    response = await authenticated_ac.post(f"/lendings/lend_book", json={
        "lend_time": "2000-01-01",
        "return_time": "2000-02-01",
        "book_id": 1,
    })

    assert response.status_code == 201

    response = await authenticated_ac.get(f"/lendings/current_user")

    assert response.status_code == 200
    assert response.json()[0]["book_id"] == 1

    response = await authenticated_ac.delete(f"/lendings/return_book/{1}")

    assert response.status_code == 200
