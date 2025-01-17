from sqlalchemy import Column, Integer, Date, ForeignKey
from app.database import Base


class Lending(Base):
    __tablename__ = "lendings"

    id = Column(Integer, primary_key=True)
    lend_time = Column(Date, nullable=False)
    return_time = Column(Date, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
