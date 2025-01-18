from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends

from app.books.dao import BookDAO
from app.schemas import SBook
from app.books.schemas import SBookAdd, BookFilter
from app.users.dependencies import get_current_admin
from app.users.models import User

router = APIRouter(
    prefix="/books",
    tags=["Книги"],
)


@router.get("/by_id/{id}")
async def get_book_by_id(
        id: int,
) -> Optional[SBook]:
    return await BookDAO.find_one_or_none(id=id)


@router.get("")
async def get_books() -> List[SBook]:
    return await BookDAO.find_all()


@router.post("", status_code=201)
async def add_book(
        data: SBookAdd,
        user: User = Depends(get_current_admin),
):
    return await BookDAO.add(**dict(data))


@router.post("/{id}")
async def update_book(
        id: int,
        data: SBookAdd,
        user: User = Depends(get_current_admin),
):
    return await BookDAO.update(id, **dict(data))


@router.delete("/{id}")
async def delete_book(
        id: int,
        user: User = Depends(get_current_admin),
):
    return await BookDAO.delete(id=id)


@router.get("/filter")
async def filter_books(
        book_filter: BookFilter = FilterDepends(BookFilter),
        page: int = Query(ge=0, default=0),
        size: int = Query(ge=1, le=100, default=10),
):# -> List[SBook]:
    return await BookDAO.filter(book_filter, page, size)
