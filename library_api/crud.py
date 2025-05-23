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


def get_all_books(
    page: int = 1,
    page_size: int = 10,
    title: Optional[str] = None,
    category: Optional[str] = None,
    sort_by: Optional[str] = None,
    desc_order: bool = False
) -> Tuple[List[Book], int]:
    """
    A unified search function that combines pagination, sorting, category filtering, and title search
    Args:
        page (int): The page number (default: 1)
        page_size (int): Number of items per page (default: 10)
        title (Optional[str]): Search books by title (case-insensitive)
        category (Optional[str]): Filter books by category
        sort_by (Optional[str]): Sort by 'year', 'author', or 'title'
        desc_order (bool): Sort in descending order if True
    Returns:
        Tuple[List[Book], int]: Tuple containing the list of books and total count
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

    # Apply sorting if provided (default to title if not specified)
    sort_field = valid_sort_fields.get(sort_by or 'title')
    if sort_field:
        query = query.order(sort_field, desc=desc_order)
    
    # Get total count before pagination
    count_result = query.execute()
    total_count = len(count_result.data)
    
    # Apply pagination
    offset = (page - 1) * page_size
    query = query.range(offset, offset + page_size - 1)

    # Execute final query
    result = query.execute()
    return [Book(**book) for book in result.data], total_count