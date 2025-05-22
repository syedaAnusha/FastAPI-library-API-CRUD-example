# FastAPI Library API CRUD Example

A simple REST API for managing a library's book collection built with FastAPI.

For more information about FastAPI, visit the [official documentation](https://fastapi.tiangolo.com/#create-it).

## Features

- CRUD operations for managing books
- Supabase PostgreSQL database integration
- CORS support for frontend integration
- Request logging and timing middleware
- Swagger UI documentation
- Rate limiting protection using slowapi (100 requests/minute for list operations, 50 requests/minute for single book operations)

## Project Structure

```
library_api/
├── crud.py         # CRUD operations with Supabase
├── database.py     # Supabase client configuration
├── main.py         # FastAPI application and routes
├── middleware.py   # Custom middleware implementations
└── models.py       # Pydantic models for data validation
```

## Setup and Installation

1. Clone this repository:

```bash
git clone https://github.com/syedaAnusha/FastAPI-library-API-CRUD-example.git
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up your environment variables in a `.env` file:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

5. Navigate to the library_api directory and run the application:

```bash
cd library_api
fastapi dev main.py --port 8001
```

The API will be available at `http://127.0.0.1:8001/`

## API Endpoints

| Method | Endpoint                     | Description                                                      |
| ------ | ---------------------------- | ---------------------------------------------------------------- |
| POST   | `/books/`                    | Create a new book                                                |
| GET    | `/books/`                    | Get paginated books (query params: page, page_size)              |
| GET    | `/books/{book_id}`           | Get a specific book by ID                                        |
| PUT    | `/books/{book_id}`           | Update a book                                                    |
| DELETE | `/books/{book_id}`           | Delete a book                                                    |
| GET    | `/books/sort/{sort_by}`      | Get books sorted by field (year, author, or title)               |
| GET    | `/books/category/{category}` | Get all books in a specific category                             |
| GET    | `/books/search/{title}`      | Basic search by title only                                       |
| GET    | `/books/combined`            | Advanced search with multiple filters (title, category, sorting) |

## Data Model

Book structure:

```json
{
    "id": int,
    "title": string,
    "author": string,
    "published_year": int,
    "category": str,
    "description": str,
    "cover_image": str,
}
```

## API Documentation

Once the server is running, you can access:

- Interactive API documentation (Swagger UI) at `http://127.0.0.1:8001/docs`
- Alternative API documentation (ReDoc) at `http://127.0.0.1:8001/redoc`

## Requirements

- Python 3.6+
- FastAPI[standard]
- Uvicorn
- Pydantic
- SQLAlchemy
- SQLModel
- psycopg2-binary
- python-dotenv
- supabase
- slowapi
