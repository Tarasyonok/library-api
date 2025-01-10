from sqlalchemy import Column, Integer, String, Date
from app.database import Base


class Authors(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    birthday = Column(Date, nullable=False)
