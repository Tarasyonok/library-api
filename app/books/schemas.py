from datetime import date
from typing import List, Optional

from fastapi_filter.contrib.sqlalchemy.filter import Filter
from pydantic import Field

from app.books.models import Book
from app.schemas import BookBase


class SBookAdd(BookBase):
    authors: List[int]


class BookFilter(Filter):
    name__like: Optional[str] = Field(alias="name", default='')
    genres__in: Optional[list[str]] = Field(alias="genres", default='')
    description__like: str = Field(alias="description", default='')
    pub_date__lte: date = Field(alias="publish_after", default=date(1, 1, 1))
    pub_date__gte: Optional[date] = Field(alias="publish_before", default=date(5000, 1, 1))
    amount__lte: int = Field(alias="amount_less_than", default=100)
    amount__gte: int = Field(alias="amount_more_than", default=0)

    class Constants(Filter.Constants):
        model = Book

    class Config:
        populate_by_name = True
