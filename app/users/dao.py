from app.users.models import User
from app.dao.base import BaseDAO


class BookDAO(BaseDAO):
    model = User
