from typing import List, Optional

from fastapi import APIRouter, Response, Depends

from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.dao import UserDAO
from app.schemas import SUser
from app.users.dependencies import get_current_user, get_current_admin
from app.users.models import User
from app.users.schemas import SUserRegister, SUserLogin, SUserChange
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
async def register_user(data: SUserRegister):
    existing_user = await UserDAO.find_one_or_none(email=data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(data.password)
    new_user = await UserDAO.add(email=data.email, hashed_password=hashed_password, role=data.role)


@auth_router.post("/login")
async def login_user(response: Response, data: SUserLogin):
    user = await authenticate_user(email=data.email, password=data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("library_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@auth_router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("library_access_token")


@router.get("/profile/view")
async def view_profile(user: User = Depends(get_current_user)) -> SUser:
    return user


@router.post("/profile/change")
async def change_profile(
        data: SUserChange,
        user: User = Depends(get_current_user)
):
    hashed_password = get_password_hash(data.password)
    data = dict(data)
    data['hashed_password'] = hashed_password
    del data['password']
    return await UserDAO.update(user.id, **data)


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
        data: SUserRegister,
        user: User = Depends(get_current_admin),
):
    existing_user = await UserDAO.find_one_or_none(email=data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(data.password)
    new_user = await UserDAO.add(email=data.email, hashed_password=hashed_password, role=data.role)


@router.post("/{id}")
async def update_user(
        id: int,
        data: SUserChange,
        user: User = Depends(get_current_admin),
):
    hashed_password = get_password_hash(data.password)
    data = dict(data)
    data['hashed_password'] = hashed_password
    del data['password']
    return await UserDAO.update(id, **data)


@router.delete("/{id}")
async def delete_user(
        id: int,
        user: User = Depends(get_current_admin),
):
    return await UserDAO.delete(id=id)
