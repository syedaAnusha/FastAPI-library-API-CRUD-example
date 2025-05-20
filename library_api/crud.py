from typing import Optional, Tuple, List
from models import BookCreate, Book
from database import supabase

def create_book(book_item: BookCreate) -> Book:
    """
    Create a new book and add it to the database.
    """
    data = dict(book_item)
    result = supabase.table('books').insert(data).execute()
    return Book(**result.data[0])

def get_all_books() -> List[Book]:
    """
    Retrieve all books from the database.
    """
    result = supabase.table('books').select('*').execute()
    return [Book(**book) for book in result.data]

def get_book_by_id(book_id: int) -> Book | None:
    """
    Retrieve a book by its ID.
    """
    result = supabase.table('books').select('*').eq('id', book_id).execute()
    return Book(**result.data[0]) if result.data else None

def update_book(book_id: int, book_item: BookCreate) -> Book | None:
    """
    Update an existing book in the database.
    """
    data = dict(book_item)
    result = supabase.table('books').update(data).eq('id', book_id).execute()
    return Book(**result.data[0]) if result.data else None

def delete_book(book_id: int) -> bool:
    """
    Delete a book from the database.
    """
    result = supabase.table('books').delete().eq('id', book_id).execute()
    return bool(result.data)

def get_sorted_books(sort_by: str, desc_order: bool = False) -> List[Book]:
    """
    Get all books sorted by the specified field.
    sort_by can be 'year', 'author', or 'title'
    """
    valid_sort_fields = {
        'year': 'published_year',
        'author': 'author',
        'title': 'title'
    }
    
    if sort_by not in valid_sort_fields:
        raise ValueError(f"Invalid sort field. Must be one of: {', '.join(valid_sort_fields.keys())}")
    
    query = supabase.table('books').select('*')
    order = valid_sort_fields[sort_by]
    
    if desc_order:
        query = query.order(order, desc=True)
    else:
        query = query.order(order)
        
    result = query.execute()
    return [Book(**book) for book in result.data]

def get_books_by_category(category: str) -> Tuple[List[Book], int]:
    """
    Get all books in a specific category and return them along with the count
    """
    result = supabase.table('books').select('*').eq('category', category).execute()
    books = [Book(**book) for book in result.data]
    return books, len(books)

def search_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None
) -> List[Book]:
    """
    Search books by title, author, or year
    """
    query = supabase.table('books').select('*')
    
    if title:
        query = query.ilike('title', f'%{title}%')
    if author:
        query = query.ilike('author', f'%{author}%')
    if year:
        query = query.eq('published_year', year)
    
    result = query.execute()
    return [Book(**book) for book in result.data]