from datetime import date
from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr


class AuthorBase(BaseModel):
    name: str
    bio: str
    birthday: date

    class Config:
        orm_mode = True


class SAuthorAdd(AuthorBase):
    books: List[int]


class UserBase(BaseModel):
    email: EmailStr
    role: Literal["R", "A"]

    class Config:
        orm_mode = True


class SUserAdd(UserBase):
    password: str


class BookBase(BaseModel):
    name: str
    description: str
    pub_date: date
    genres: List[str]
    amount: int

    class Config:
        orm_mode = True


class SBookAdd(BookBase):
    authors: List[int]
    users: List[int]


class SAuthor(AuthorBase):
    id: int
    books: List[BookBase]


class SUser(UserBase):
    id: int
    books: List[BookBase]


class SBook(BookBase):
    id: int
    authors: List[AuthorBase]
    users: List[UserBase]
