from typing import List, Optional

from fastapi import APIRouter

from app.authors.dao import AuthorDAO
from app.authors.schemas import SAuthor

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


@router.post("")
async def add_author(
        data: SAuthor,
) -> int:
    return await AuthorDAO.add(data)


@router.post("/{id}")
async def update_author(
        id: int,
        data: SAuthor,
):
    return await AuthorDAO.update(id, data)


@router.delete("/{id}")
async def delete_author(
        id: int,
):
    return await AuthorDAO.delete(id=id)
