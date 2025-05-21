from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, Tuple, List
from pydantic import BaseModel
from .models import Book, BookCreate, PaginatedResponse, CategoryResponse
from .crud import create_book, get_all_books, get_book_by_id, update_book, delete_book, get_sorted_books, get_books_by_category, search_books
from .middleware import logging_middleware
from starlette.middleware.proxy_headers import ProxyHeadersMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Library API",
             description="A simple REST API for managing a library's book collection")

# Add rate limiter to the application
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

FRONT_END_URLS = os.getenv("ALLOWED_ORIGINS").split(',')
origins = [url.strip() for url in FRONT_END_URLS if url.strip()]
# Since Railway handles HTTPS, we don't need custom HTTPS redirect middleware
# Just configure CORS properly

# Add before other middlewares
app.add_middleware(ProxyHeadersMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Type", "Authorization"],
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
def create_book_endpoint(book_item: BookCreate):
    """
    Create a new book and add it to the database.
    """
    return create_book(book_item)

@app.get("/books/", response_model=PaginatedResponse)
@limiter.limit("100/minute")  # Rate limit: 100 requests per minute
async def read_books(
    request: Request,  # Required for rate limiting
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page")
):
    """
    Retrieve books from the database with pagination.
    Rate limited to 100 requests per minute.
    Results are cached for 60 seconds.
    """
    books, total = get_all_books(page, page_size)
    return PaginatedResponse(books=books, total=total)

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

@app.get("/books/sort/{sort_by}")
def get_sorted_books_endpoint(
    sort_by: str,
    desc: bool = Query(False, description="Sort in descending order")
):
    """
    Get books sorted by specified field (year, author, or title)
    """
    try:
        return get_sorted_books(sort_by, desc)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/books/category/{category}", response_model=CategoryResponse)
def get_books_by_category_endpoint(category: str):
    """
    Get all books in a specific category and their count
    """
    books, count = get_books_by_category(category)
    return CategoryResponse(books=books, total=count)

@app.get("/books/search/{title}")
def search_books_endpoint(title: str):
    """
    Search books by title
    """
    return search_books(title)