from datetime import date
from typing import List, Optional

from fastapi_filter.contrib.sqlalchemy.filter import Filter
from pydantic import Field

from app.authors.models import Author
from app.schemas import AuthorBase


class SAuthorAdd(AuthorBase):
    books: List[int]


class AuthorFilter(Filter):
    name__like: Optional[str] = Field(alias="name", default='')
    bio__like: str = Field(alias="bio", default='')
    birthday__lte: date = Field(alias="older_than", default=date(1, 1, 1))
    birthday__gte: Optional[date] = Field(alias="younger_than", default=date(5000, 1, 1))

    class Constants(Filter.Constants):
        model = Author

    class Config:
        populate_by_name = True
