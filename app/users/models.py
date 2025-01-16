from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from app.database import Base


class User(Base):
    ROLE_CHOICES = (
        ("R", "Reader"),
        ("A", "Admin"),
    )

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    about = Column(String, nullable=True)
    role = Column(ChoiceType(ROLE_CHOICES), nullable=False)

    books = relationship('Book', secondary='users_books', back_populates='users', lazy="selectin")


class UserBook(Base):
    __tablename__ = "users_books"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
