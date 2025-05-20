from pydantic import BaseModel
from typing import Optional

# Pydantic Models for API

# BookBase defines the common fields that all book-related models share
class BookBase(BaseModel):
    title: str
    author: str
    published_year: int
    category: str
    description: str
    cover_image: str

# BookCreate is used specifically for input validation when creating 
# new books (it doesn't include an ID since it hasn't been created yet)
class BookCreate(BookBase):
    pass

# Book extends the base model to include the id field, 
# which is used when returning books from the API 
# (since they'll have an ID after being stored in the database)
class Book(BookBase):
    id: int

    class Config:
        from_attributes = True # Allows conversion from ORM models to Pydantic models