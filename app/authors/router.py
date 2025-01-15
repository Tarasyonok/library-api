from typing import List, Optional

from fastapi import APIRouter

from app.authors.dao import AuthorDAO
from app.schemas import SAuthor, SAuthorAdd

router = APIRouter(
    prefix="/authors",
    tags=["Авторы"],
)


@router.get("/{id}")
async def get_author_by_id(
        id: int,
) -> Optional[SAuthor]:
    return await AuthorDAO.find_one_or_none(id=id)


@router.get("")
async def get_authors() -> List[SAuthor]:
    return await AuthorDAO.find_all()


@router.post("", status_code=201)
async def add_author(
        data: SAuthorAdd,
):
    return await AuthorDAO.add(**dict(data))


@router.post("/{id}")
async def update_author(
        id: int,
        data: SAuthorAdd,
):
    return await AuthorDAO.update(id, **dict(data))


@router.delete("/{id}")
async def delete_author(
        id: int,
):
    return await AuthorDAO.delete(id=id)
