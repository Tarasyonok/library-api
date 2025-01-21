from sqlalchemy import Column, Integer, Date, ForeignKey, Sequence
from app.database import Base


class Lending(Base):
    __tablename__ = "lendings"

    id_lendings_seq = Sequence("id_lendings_seq", start=101)
    id = Column(Integer, id_lendings_seq, server_default=id_lendings_seq.next_value(), primary_key=True)

    lend_time = Column(Date, nullable=False)
    return_time = Column(Date, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
