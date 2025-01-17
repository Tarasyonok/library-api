from typing import List, Optional

from fastapi import APIRouter, Depends

from app.lendings.dao import LendingDAO
from app.lendings.schemas import SLending, SLendBook
from app.users.dependencies import get_current_admin, get_current_user
from app.users.models import User

router = APIRouter(
    prefix="/lendings",
    tags=["Выдача и возврат книг"],
)


@router.get("/by_id/{id}")
async def get_lending_by_id(
        id: int,
        user: User = Depends(get_current_admin),
) -> Optional[SLending]:
    return await LendingDAO.find_by_id(id=id)


@router.get("")
async def get_all_lendings(
        user: User = Depends(get_current_admin),
) -> List[SLending]:
    return await LendingDAO.find_all()


@router.get("/current_user")
async def get_user_lendings(
        user: User = Depends(get_current_user),
) -> List[SLending]:
    return await LendingDAO.find_all(user_id=user.id)


@router.post("/lend_book", status_code=201)
async def lend_book(
        data: SLendBook,
        user: User = Depends(get_current_user),
):
    data = dict(data)
    data['user_id'] = user.id
    return await LendingDAO.lend_book(**data)


@router.delete("/return_book/{id}")
async def return_book(
        id: int,
        user: User = Depends(get_current_user),
):
    return await LendingDAO.return_book(book_id=id, user_id=user.id)


@router.delete("/{id}")
async def delete_lending(
        id: int,
        user: User = Depends(get_current_admin),
):
    return await LendingDAO.return_book_via_id(id=id)
