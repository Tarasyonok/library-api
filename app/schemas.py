from datetime import date
from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict


class AuthorBase(BaseModel):
    name: str
    bio: str
    birthday: date

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr
    role: Literal["R", "A"]
    name: Optional[str]
    about: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    name: str
    description: str
    pub_date: date
    genres: List[str]
    amount: int

    model_config = ConfigDict(from_attributes=True)


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
