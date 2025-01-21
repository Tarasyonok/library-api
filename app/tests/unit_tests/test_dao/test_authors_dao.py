from datetime import date

import pytest

from app.authors.dao import AuthorDAO


@pytest.mark.parametrize("id,does_exist", [
    (1, True),
    (2, True),
    (999, False),
])
async def test(id, does_exist):
    author = await AuthorDAO.find_one_or_none(id=id)

    if does_exist:
        assert author
        assert author.id == id
    else:
        assert not author


async def test_find_all():
    authors = await AuthorDAO.find_all()

    assert isinstance(authors, list)


async def test_add_correct():
    author_id = await AuthorDAO.add(
        name="test",
        bio="test",
        birthday=date(2000, 1, 1),
        books=[],
    )

    author = await AuthorDAO.find_one_or_none(id=author_id)

    assert author
    assert author.name == "test"


async def test_add_incorrect():
    try:
        author_id = await AuthorDAO.add(
            name=None,
            bio="test",
            birthday=date(2000, 1, 1),
            books=[],
        )
    except Exception:
        author_id = None

    assert not author_id


async def test_delete():
    author_id = await AuthorDAO.delete(name="test")
    author = await AuthorDAO.find_one_or_none(id=author_id)
    assert not author
