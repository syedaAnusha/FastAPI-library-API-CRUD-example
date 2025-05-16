from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from database import Base

# SQLAlchemy Model
class BookDB(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    published_year = Column(Integer)

# Pydantic Models for API
class BookBase(BaseModel):
    title: str
    author: str
    published_year: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True