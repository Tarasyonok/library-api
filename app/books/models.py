from sqlalchemy import Column, Integer, String, Date, JSON
from sqlalchemy.orm import relationship

from app.database import Base
from app.users.models import User


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    pub_date = Column(Date, nullable=False)
    genres = Column(JSON, nullable=True)
    amount = Column(Integer, nullable=False)

    authors = relationship('Author', secondary='authors_books', back_populates='books', lazy="selectin")
    users = relationship('User', secondary='users_books', back_populates='books', lazy="selectin")
