from datetime import date
from typing import List, Literal

from pydantic import BaseModel

import app.books.schemas as books_schemas


class UserBase(BaseModel):
    id: int
    nickname: str
    role: Literal["R", "A"]

    class Config:
        orm_mode = True


class SUser(UserBase):
    books: List[books_schemas.BookBase]
