from datetime import date
from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr


class AuthorBase(BaseModel):
    name: str
    bio: str
    birthday: date

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr
    role: Literal["R", "A"]
    name: Optional[str]
    about: Optional[str]

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    name: str
    description: str
    pub_date: date
    genres: List[str]
    amount: int

    class Config:
        from_attributes = True


class SBookAdd(BookBase):
    authors: List[int]


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
