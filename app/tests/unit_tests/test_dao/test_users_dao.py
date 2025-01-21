from datetime import date

import pytest

from app.users.auth import get_password_hash
from app.users.dao import UserDAO


@pytest.mark.parametrize("id,does_exist", [
    (1, True),
    (2, True),
    (999, False),
])
async def test(id, does_exist):
    user = await UserDAO.find_one_or_none(id=id)

    if does_exist:
        assert user
        assert user.id == id
    else:
        assert not user


async def test_find_all():
    users = await UserDAO.find_all()

    assert isinstance(users, list)


async def test_add_correct():
    password = "qwerty"
    hashed_password = get_password_hash(password)
    user_id = await UserDAO.add(
        email="user@user.com",
        hashed_password=hashed_password,
        role="R",
    )

    user = await UserDAO.find_one_or_none(id=user_id)

    assert user
    assert user.email == "user@user.com"


async def test_add_incorrect():
    try:
        user_id = await UserDAO.add(
            email=None,
            hashed_password=None,
            role="R",
        )
    except Exception:
        user_id = None

    assert not user_id


async def test_delete():
    user_id = await UserDAO.delete(email="user@user.com")
    user = await UserDAO.find_one_or_none(id=user_id)
    assert not user
