from pydantic import BaseModel, EmailStr
from typing import Literal


class SUserRegister(BaseModel):
    email: EmailStr
    password: str
    role: Literal["R", "A"]

    class Config:
        orm_mode = True


class SUserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class SUserChange(BaseModel):
    email: EmailStr
    password: str
    name: str
    about: str

    class Config:
        orm_mode = True
