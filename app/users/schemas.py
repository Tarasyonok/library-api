from pydantic import BaseModel, EmailStr
from typing import Literal

from pydantic import ConfigDict


class SUserRegister(BaseModel):
    email: EmailStr
    password: str
    role: Literal["R", "A"]

    model_config = ConfigDict(from_attributes=True)


class SUserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class SUserChange(BaseModel):
    email: EmailStr
    password: str
    name: str
    about: str

    model_config = ConfigDict(from_attributes=True)
