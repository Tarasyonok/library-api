from datetime import date
from pydantic import BaseModel

from app.schemas import UserBase, BookBase


class SLendingBase(BaseModel):
    lend_time: date
    return_time: date

    class Config:
        from_attributes = True


class SLendBook(SLendingBase):
    book_id: int


class SLending(SLendingBase):
    id: int
    user_id: int
    book_id: int
