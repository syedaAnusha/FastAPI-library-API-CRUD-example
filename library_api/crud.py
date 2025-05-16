from sqlalchemy.orm import Session
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