from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, Tuple, List
from pydantic import BaseModel
from .models import Book, BookCreate, PaginatedResponse, CategoryResponse
from .crud import (
    create_book, get_book_by_id, update_book, delete_book, get_all_books
)
from .middleware import logging_middleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Library API",
             description="A simple REST API for managing a library's book collection")

FRONT_END_URLS = os.getenv("ALLOWED_ORIGINS").split(',')
origins = [url.strip() for url in FRONT_END_URLS if url.strip()]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Type", "Authorization"],
)

# Add rate limiter to the application
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
                "list_books": "GET /books/combined",
                "create_book": "POST /books/",
                "get_book": "GET /books/{book_id}",
                "update_book": "PUT /books/{book_id}",
                "delete_book": "DELETE /books/{book_id}"
            }
        }
    })

@app.post("/books/", response_model=Book)
def create_book_endpoint(book_item: BookCreate):
    """
    Create a new book and add it to the database.
    """
    return create_book(book_item)

@app.get("/books/combined", response_model=PaginatedResponse)
@limiter.limit("50/minute")
async def get_all_books_combined(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    title: Optional[str] = Query(None, description="Search by title (case-insensitive)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    sort_by: Optional[str] = Query(None, description="Sort by 'year', 'author', or 'title'"),
    desc: bool = Query(False, description="Sort in descending order")
):
    """
    Unified search endpoint that combines:
    - Pagination
    - Title search
    - Category filtering
    - Sorting by year, author, or title (defaults to title)
    All parameters are optional, allowing for flexible querying.
    Rate limited to 50 requests per minute.
    """
    try:
        books, total = get_all_books(
            page=page,
            page_size=page_size,
            title=title,
            category=category,
            sort_by=sort_by,
            desc_order=desc
        )
        return PaginatedResponse(books=books, total=total)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/books/{book_id}", response_model=Book)
@limiter.limit("50/minute")  # Rate limit: 50 requests per minute
async def read_book(request: Request, book_id: int):
    """
    Retrieve a book by its ID.
    Rate limited to 50 requests per minute.
    Results are cached for 5 minutes.
    """
    book = get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=Book)
def update_book_endpoint(book_id: int, book_item: BookCreate):
    """
    Update an existing book.
    """
    book = update_book(book_id, book_item)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/books/{book_id}")
def delete_book_endpoint(book_id: int):
    """
    Delete a book.
    """
    success = delete_book(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
