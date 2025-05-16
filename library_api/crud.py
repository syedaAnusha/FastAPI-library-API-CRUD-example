from models import Book, BookCreate
from database import books

def create_book(book_item: BookCreate) -> Book:
    """
    Create a new book and add it to the database.
    """
    new_book = Book(id=len(books) + 1, **book_item.dict())
    books.append(new_book)
    return new_book

def get_all_books() -> list[Book]:
    """
    Retrieve all books from the database.
    """
    return books

def get_book_by_id(book_id: int) -> Book | None:
    """
    Retrieve a book by its ID.
    """
    for book in books:
        if book.id == book_id:
            return book
    return None

def update_book(book_id: int, book_item: BookCreate) -> Book | None:
    """
    Update an existing book in the database.
    """
    for index, book in enumerate(books):
        if book.id == book_id:
            updated_book = Book(id=book_id, **book_item.dict())
            books[index] = updated_book
            return updated_book
    return None

def delete_book(book_id: int) -> Book:
    """
    Delete a book from the database.
    """
    for index, book in enumerate(books):
        if book.id == book_id:
            return books.pop(index)
    return False