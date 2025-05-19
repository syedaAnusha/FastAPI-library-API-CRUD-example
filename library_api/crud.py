from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, Tuple
from models import BookDB, BookCreate, Book

def create_book(db: Session, book_item: BookCreate) -> Book:
    """
    Create a new book and add it to the database.
    """
    db_book = BookDB(**book_item.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_all_books(db: Session) -> list[Book]:
    """
    Retrieve all books from the database.
    """
    return db.query(BookDB).all()

def get_book_by_id(db: Session, book_id: int) -> Book | None:
    """
    Retrieve a book by its ID.
    """
    return db.query(BookDB).filter(BookDB.id == book_id).first()

def update_book(db: Session, book_id: int, book_item: BookCreate) -> Book | None:
    """
    Update an existing book in the database.
    """
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if db_book:
        for key, value in book_item.dict().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int) -> bool:
    """
    Delete a book from the database.
    """
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False

def get_sorted_books(db: Session, sort_by: str, desc_order: bool = False) -> list[Book]:
    """
    Get all books sorted by the specified field.
    sort_by can be 'year', 'author', or 'title'
    """
    valid_sort_fields = {
        'year': BookDB.published_year,
        'author': BookDB.author,
        'title': BookDB.title
    }
    
    if sort_by not in valid_sort_fields:
        raise ValueError(f"Invalid sort field. Must be one of: {', '.join(valid_sort_fields.keys())}")
    
    query = db.query(BookDB)
    if desc_order:
        query = query.order_by(desc(valid_sort_fields[sort_by]))
    else:
        query = query.order_by(valid_sort_fields[sort_by])
    
    return query.all()

def get_books_by_category(db: Session, category: str) -> Tuple[list[Book], int]:
    """
    Get all books in a specific category and return them along with the count
    """
    query = db.query(BookDB).filter(BookDB.category == category)
    books = query.all()
    count = query.count()
    return books, count

def search_books(
    db: Session,
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None
) -> list[Book]:
    """
    Search books by title, author, or year
    """
    query = db.query(BookDB)
    
    if title:
        query = query.filter(BookDB.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(BookDB.author.ilike(f"%{author}%"))
    if year:
        query = query.filter(BookDB.published_year == year)
    
    return query.all()