from typing import List, Optional

from fastapi import APIRouter, HTTPException, Response

from app.users.dao import UserDAO
from app.schemas import SUser
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
#
#
# @auth_router.post("/logout")
# async def logout_user(response: Response):
#     response.delete_cookie("booking_access_token")
