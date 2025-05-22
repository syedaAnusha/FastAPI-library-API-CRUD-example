from .models import BookCreate, Book
from .database import supabase
from typing import Optional, Tuple, List

def create_book(book_item: BookCreate) -> Book:
    """
    Create a new book and add it to the database.
    """
    data = dict(book_item)
    result = supabase.table('books').insert(data).execute()
    return Book(**result.data[0])

def get_all_books(page: int = 1, page_size: int = 10) -> Tuple[List[Book], int]:
    """
    Retrieve books from the database with pagination.
    Args:
        page (int): The page number (default: 1)
        page_size (int): Number of items per page (default: 10)
    Returns:
        Tuple[List[Book], int]: A tuple containing the list of books and total count
    """
    # First get total count
    count_result = supabase.table('books').select('count', count='exact').execute()
    total_count = count_result.count if hasattr(count_result, 'count') else 0
    
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Get paginated results
    result = supabase.table('books').select('*').range(offset, offset + page_size - 1).execute()
    books = [Book(**book) for book in result.data]
    
    return books, total_count

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

def search_books(title: str) -> List[Book]:
    """
    Search books by title
    """
    result = supabase.table('books').select('*').ilike('title', f'%{title}%').execute()
    return [Book(**book) for book in result.data]

def search_books_combined(
    title: Optional[str] = None,
    category: Optional[str] = None,
    sort_by: Optional[str] = None,
    desc_order: bool = False
) -> List[Book]:
    """
    A unified search function that combines sorting, category filtering, and title search
    Args:
        title (Optional[str]): Search books by title (case-insensitive)
        category (Optional[str]): Filter books by category
        sort_by (Optional[str]): Sort by 'year', 'author', or 'title'
        desc_order (bool): Sort in descending order if True
    Returns:
        List[Book]: List of books matching the criteria
    """
    valid_sort_fields = {
        'year': 'published_year',
        'author': 'author',
        'title': 'title'
    }

    # Start with base query
    query = supabase.table('books').select('*')

    # Apply title search if provided
    if title:
        query = query.ilike('title', f'%{title}%')

    # Apply category filter if provided
    if category:
        query = query.eq('category', category)

    # Apply sorting if provided
    if sort_by:
        if sort_by not in valid_sort_fields:
            raise ValueError(f"Invalid sort field. Must be one of: {', '.join(valid_sort_fields.keys())}")
        order = valid_sort_fields[sort_by]
        query = query.order(order, desc=desc_order)

    result = query.execute()
    return [Book(**book) for book in result.data]