from typing import List, Optional

from fastapi import APIRouter, Depends

from app.books.dao import BookDAO
from app.schemas import SBook, SBookAdd
from app.users.dependencies import get_current_admin
from app.users.models import User

router = APIRouter(
    prefix="/books",
    tags=["Книги"],
)


@router.get("/{id}")
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
