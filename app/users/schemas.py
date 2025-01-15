from pydantic import BaseModel, EmailStr
from typing import Literal

class SUserRegister(BaseModel):
    email: EmailStr
    password: str
    role: Literal["R", "A"]


class SUserLogin(BaseModel):
    email: EmailStr
    password: str
