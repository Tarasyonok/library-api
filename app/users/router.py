from typing import List, Optional

from fastapi import APIRouter, HTTPException, Response, Depends

from app.users.dao import UserDAO
from app.schemas import SUser, SUserAdd
from app.users.dependencies import get_current_user, get_current_admin
from app.users.models import User
from app.users.schemas import SUserRegister, SUserLogin
from app.users.auth import get_password_hash, authenticate_user, create_access_token

auth_router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@auth_router.post("/register", status_code=201)
async def register_user(user_data: SUserRegister):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500)
    hashed_password = get_password_hash(user_data.password)
    new_user = await UserDAO.add(email=user_data.email, hashed_password=hashed_password, role=user_data.role)


@auth_router.post("/login")
async def login_user(response: Response, user_data: SUserLogin):
    user = await authenticate_user(email=user_data.email, password=user_data.password)
    if not user:
        raise HTTPException(status_code=401)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("library_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@auth_router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/me")
async def me(user: User = Depends(get_current_user)) -> Optional[SUser]:
    return user


@router.get("/all")
async def get_(user: User = Depends(get_current_admin)) -> List[SUser]:
    return await UserDAO.find_all()


@router.get("/{id}")
async def get_user_by_id(
        id: int,
        user: User = Depends(get_current_admin),
) -> Optional[SUser]:
    return await UserDAO.find_one_or_none(id=id)


@router.get("")
async def get_users(
        user: User = Depends(get_current_admin),
) -> List[SUser]:
    return await UserDAO.find_all()


@router.post("", status_code=201)
async def add_user(
        data: SUserAdd,
        user: User = Depends(get_current_admin),
):
    return await UserDAO.add(**dict(data))


@router.post("/{id}")
async def update_user(
        id: int,
        data: SUserAdd,
        user: User = Depends(get_current_admin),
):
    return await UserDAO.update(id, **dict(data))


@router.delete("/{id}")
async def delete_user(
        id: int,
        user: User = Depends(get_current_admin),
):
    return await UserDAO.delete(id=id)
