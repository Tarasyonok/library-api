from app.authors.models import Author
from app.dao.base import BaseDAO


class AuthorDAO(BaseDAO):
    model = Author
