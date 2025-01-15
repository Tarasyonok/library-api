from fastapi import Depends, Request, HTTPException
from jose import ExpiredSignatureError, JWTError, jwt

from app.config import settings
from app.users.dao import UserDAO
from app.users.models import User


def get_token(request: Request):
    token = request.cookies.get("library_access_token")
    if not token:
        raise HTTPException(status_code=401)
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except ExpiredSignatureError:
        # Как позже выяснилось, ключ exp автоматически проверяется
        # командой jwt.decode, поэтому отдельно проверять это не нужно
        raise HTTPException(status_code=500)
    except JWTError:
        raise HTTPException(status_code=500)
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=500)
    user = await UserDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise HTTPException(status_code=500)

    return user


async def get_current_admin(user: User = Depends(get_current_user)):
    if user.role != "A":
        raise HTTPException(status_code=500)
    return user

