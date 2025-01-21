from datetime import date

import pytest

from app.books.dao import BookDAO


@pytest.mark.parametrize("id,does_exist", [
    (1, True),
    (2, True),
    (999, False),
])
async def test(id, does_exist):
    book = await BookDAO.find_one_or_none(id=id)

    if does_exist:
        assert book
        assert book.id == id
    else:
        assert not book


async def test_find_all():
    books = await BookDAO.find_all()

    assert isinstance(books, list)


async def test_add_correct():
    book_id = await BookDAO.add(
        name="test",
        description="test",
        pub_date=date(2000, 1, 1),
        genres=["test"],
        authors=[],
        amount=1,
    )

    book = await BookDAO.find_one_or_none(id=book_id)

    assert book
    assert book.name == "test"


async def test_add_incorrect():
    try:
        book_id = await BookDAO.add(
            name=None,
            description="test",
            pub_date=date(2000, 1, 1),
            genres=["test"],
            authors=[],
            amount=1,
        )
    except Exception:
        book_id = None

    assert not book_id


async def test_delete():
    book_id = await BookDAO.delete(name="test")
    book = await BookDAO.find_one_or_none(id=book_id)
    assert not book
