from datetime import date
from typing import List

from pydantic import BaseModel

from app.books.models import Book


class SAuthor(BaseModel):
    id: int
    name: str
    bio: str
    birthday: date
    books: List[int]

    class Config:
        orm_mode = True
