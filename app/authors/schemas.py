from datetime import date
from typing import List

from pydantic import BaseModel

import app.books.schemas as books_schemas


class AuthorBase(BaseModel):
    id: int
    name: str
    bio: str
    birthday: date

    class Config:
        orm_mode = True

class SAuthor(AuthorBase):
    books: List[books_schemas.BookBase]

