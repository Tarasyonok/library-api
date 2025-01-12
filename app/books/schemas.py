from datetime import date
from typing import List

from pydantic import BaseModel


class BookBase(BaseModel):
    id: int
    name: str
    description: str
    pub_date: date
    genres: List[str]
    amount: int

    class Config:
        orm_mode = True


class SBook(BookBase):
    from app.authors.schemas import AuthorBase
    from app.users.schemas import UserBase

    books: List[AuthorBase]
    users: List[UserBase]
