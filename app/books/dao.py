from app.books.models import Book
from app.dao.base import BaseDAO


class BookDAO(BaseDAO):
    model = Book
