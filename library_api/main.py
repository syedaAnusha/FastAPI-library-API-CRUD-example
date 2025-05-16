from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Book, BookCreate
import crud
from database import engine, Base, get_db

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

@app.post("/books/", response_model=Book)
def create_book(book_item: BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book and add it to the database.
    """
    return crud.create_book(db, book_item)

@app.get("/books/", response_model=list[Book])
def read_books(db: Session = Depends(get_db)):
    """
    Retrieve all books from the database.
    """
    return crud.get_all_books(db)

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a book by its ID.
    """
    book = crud.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book_item: BookCreate, db: Session = Depends(get_db)):
    """
    Update an existing book.
    """
    book = crud.update_book(db, book_id, book_item)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book.
    """
    success = crud.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}