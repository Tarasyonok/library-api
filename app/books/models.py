from sqlalchemy import Column, Integer, String, Date, JSON
from sqlalchemy.orm import relationship

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    pub_date = Column(Date, nullable=False)
    authors = relationship('Author', secondary='authors_books', back_populates='books')
    genres = Column(JSON, nullable=True)
    amount = Column(Integer, nullable=False)
