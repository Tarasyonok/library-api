from sqlalchemy import Column, Integer, String, Date, ForeignKey, Sequence
from sqlalchemy.orm import relationship

from app.database import Base
from app.books.models import Book


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)

    id_authors_seq = Sequence("id_authors_seq", start=101)
    id = Column(Integer, id_authors_seq, server_default=id_authors_seq.next_value(), primary_key=True)

    name = Column(String, nullable=False, unique=True)
    bio = Column(String, nullable=True)
    birthday = Column(Date, nullable=False)

    books = relationship('Book', secondary='authors_books', back_populates='authors', lazy="selectin")


class AuthorBook(Base):
    __tablename__ = "authors_books"

    id_authors_books_seq = Sequence("id_authors_books_seq", start=101)
    id = Column(Integer, id_authors_books_seq, server_default=id_authors_books_seq.next_value(), primary_key=True)

    author_id = Column(Integer, ForeignKey('authors.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
