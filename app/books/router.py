from typing import List, Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi_filter import FilterDepends
from fastapi.responses import JSONResponse

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
) -> SBook:
    book = await BookDAO.find_one_or_none(id=id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена",
        )
    return book


@router.get("")
async def get_books() -> List[SBook]:
    return await BookDAO.find_all()


@router.post("")
async def add_book(
        data: SBookAdd,
        user: User = Depends(get_current_admin),
) -> JSONResponse:
    try:
        book_id = await BookDAO.add(**dict(data))
        return JSONResponse(f"Книга с названием {data.name} добавлена (ID {book_id})", status_code=201)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"При добавлении книги возникла непредвиденная ошибка:   {str(e)}",
        )


@router.post("/{id}")
async def update_book(
        id: int,
        data: SBookAdd,
        user: User = Depends(get_current_admin),
) -> JSONResponse:
    try:
        await BookDAO.update(id, **dict(data))
        return JSONResponse(f"Книга с названием {data.name} успешно изменена (ID {id})", status_code=200)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"При изменении книги c ID {id} возникла непредвиденная ошибка:   {str(e)}",
        )


@router.delete("/{id}")
async def delete_book(
        id: int,
        user: User = Depends(get_current_admin),
) -> JSONResponse:
    try:
        await BookDAO.delete(id=id)
        return JSONResponse(f"Книга с ID {id} успешно удалена", status_code=200)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"При удалении книги c ID {id} возникла непредвиденная ошибка:   {str(e)}",
        )


@router.get("/filter")
async def filter_books(
        book_filter: BookFilter = FilterDepends(BookFilter),
        page: int = Query(ge=0, default=0),
        size: int = Query(ge=1, le=100, default=10),
) -> List[SBook] | str:
    try:
        return await BookDAO.filter(book_filter, page, size)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"При фильтрации возникла непредвиденная ошибка:   {str(e)}",
        )
