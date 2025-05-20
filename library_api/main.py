from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, Tuple, List
from pydantic import BaseModel
from models import Book, BookCreate
import crud
from middleware import logging_middleware

app = FastAPI(title="Library API",
             description="A simple REST API for managing a library's book collection")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],  # Allow both localhost and 127.0.0.1
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Add custom logging middleware
app.middleware("http")(logging_middleware)

@app.get("/")
async def root():
    """
    Root endpoint that provides API information and available endpoints
    """
    return JSONResponse({
        "message": "Welcome to the Library API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "books": {
                "list_books": "GET /books/",
                "create_book": "POST /books/",
                "get_book": "GET /books/{book_id}",
                "update_book": "PUT /books/{book_id}",
                "delete_book": "DELETE /books/{book_id}",
                "sort_books": "GET /books/sort/{sort_by}",
                "books_by_category": "GET /books/category/{category}",
                "search_books": "GET /books/search/"
            }
        }
    })

@app.post("/books/", response_model=Book)
def create_book(book_item: BookCreate):
    """
    Create a new book and add it to the database.
    """
    return crud.create_book(book_item)

@app.get("/books/", response_model=List[Book])
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
    Update an existing book.
    """
    book = crud.update_book(book_id, book_item)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    """
    Delete a book.
    """
    success = crud.delete_book(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}

class CategoryResponse(BaseModel):
    books: List[Book]
    total: int

@app.get("/books/sort/{sort_by}")
def get_sorted_books(
    sort_by: str,
    desc: bool = Query(False, description="Sort in descending order")
):
    """
    Get books sorted by specified field (year, author, or title)
    """
    try:
        return crud.get_sorted_books(sort_by, desc)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/books/category/{category}", response_model=CategoryResponse)
def get_books_by_category(category: str):
    """
    Get all books in a specific category and their count
    """
    books, count = crud.get_books_by_category(category)
    return CategoryResponse(books=books, total=count)

@app.get("/books/search/{title}")
def search_books(title: str):
    """
    Search books by title
    """
    return crud.search_books(title)