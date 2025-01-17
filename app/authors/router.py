from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends

from app.authors.dao import AuthorDAO
from app.schemas import SAuthor
from app.authors.schemas import SAuthorAdd, AuthorFilter
from app.users.dependencies import get_current_admin
from app.users.models import User

router = APIRouter(
    prefix="/authors",
    tags=["Авторы"],
)


@router.get("/by_id/{id}")
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
        user: User = Depends(get_current_admin),
):
    return await AuthorDAO.add(**dict(data))


@router.post("/{id}")
async def update_author(
        id: int,
        data: SAuthorAdd,
        user: User = Depends(get_current_admin),
):
    return await AuthorDAO.update(id, **dict(data))


@router.delete("/{id}")
async def delete_author(
        id: int,
        user: User = Depends(get_current_admin),
):
    return await AuthorDAO.delete(id=id)


@router.get("/filter")
async def filter_authors(
        author_filter: AuthorFilter = FilterDepends(AuthorFilter),
        page: int = Query(ge=0, default=0),
        size: int = Query(ge=1, le=100, default=10),
) -> List[SAuthor]:
    return await AuthorDAO.filter(author_filter, page, size)
