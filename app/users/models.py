from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from app.database import Base

ROLE_CHOICES = (
    ('R', 'Reader'),
    ('A', 'Admin'),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nickname = Column(String, nullable=False, unique=True)
    role = ChoiceType(ROLE_CHOICES, impl=String(length=1))

    books = relationship('Book', secondary='users_books', back_populates='users')


class UserBook(Base):
    __tablename__ = "users_books"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))