from fastapi import FastAPI, HTTPException
from models import Book, BookCreate
import crud

app = FastAPI()
@app.post("/books/", response_model=Book)
def create_book(book_item: BookCreate):
    """
    Create a new book and add it to the database.
    """
    return crud.create_book(book_item)

@app.get("/books/", response_model=list[Book])
def read_books():
    """
    Retrieve all books from the database.
    """
    return crud.get_all_books()

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int):
    """
    Retrieve a book by its ID.
    """
    book = crud.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book_item: BookCreate):
    """
    Update an existing book in the database.
    """
    book = crud.update_book(book_id, book_item)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/books/{book_id}", response_model=Book)
def delete_book(book_id: int):
    """
    Delete a book from the database.
    """
    book = crud.delete_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book