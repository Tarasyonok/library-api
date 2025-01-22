from typing import List, Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi_filter import FilterDepends
from fastapi.responses import JSONResponse

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
) -> SAuthor:
    author = await AuthorDAO.find_one_or_none(id=id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Автор не найден",
        )
    return author


@router.get("")
async def get_authors() -> List[SAuthor]:
    return await AuthorDAO.find_all()


@router.post("")
async def add_author(
        data: SAuthorAdd,
        user: User = Depends(get_current_admin),
) -> JSONResponse:
    try:
        author_id = await AuthorDAO.add(**dict(data))
        return JSONResponse( {"deatil": f"Автор с именем {data.name} добавлен (ID {author_id})"}, status_code=201)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"При добавлении автора возникла непредвиденная ошибка:   {str(e)}",
        )


@router.post("/{id}")
async def update_author(
        id: int,
        data: SAuthorAdd,
        user: User = Depends(get_current_admin),
) -> JSONResponse:
    try:
        await AuthorDAO.update(id, **dict(data))
        return JSONResponse( {"deatil": f"Автор с именем {data.name} успешно изменён (ID {id})"}, status_code=200)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"При изменении автора c ID {id} возникла непредвиденная ошибка:   {str(e)}",
        )


@router.delete("/{id}")
async def delete_author(
        id: int,
        user: User = Depends(get_current_admin),
) -> JSONResponse:
    try:
        await AuthorDAO.delete(id=id)
        return JSONResponse( {"deatil": f"Автор с ID {id} успешно удалён"}, status_code=200)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"При удалении автора c ID {id} возникла непредвиденная ошибка:   {str(e)}",
        )


@router.get("/filter")
async def filter_authors(
        author_filter: AuthorFilter = FilterDepends(AuthorFilter),
        page: int = Query(ge=0, default=0),
        size: int = Query(ge=1, le=100, default=10),
) -> List[SAuthor]:
    try:
        return await AuthorDAO.filter(author_filter, page, size)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"При фильтрации возникла непредвиденная ошибка:   {str(e)}",
        )
