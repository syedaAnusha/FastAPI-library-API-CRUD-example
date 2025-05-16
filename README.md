# FastAPI Library API CRUD Example

A simple REST API for managing a library's book collection built with FastAPI.

For more information about FastAPI, visit the [official documentation](https://fastapi.tiangolo.com/#create-it).

## Features

- CRUD operations for managing books
- SQLite database with SQLAlchemy ORM
- CORS support for frontend integration
- Request logging and timing middleware
- Swagger UI documentation

## Project Structure

```
library_api/
├── crud.py         # CRUD operations with SQLAlchemy
├── database.py     # SQLite database configuration
├── library.db      # SQLite database file
├── main.py         # FastAPI application and routes
├── middleware.py   # Custom middleware implementations
└── models.py       # SQLAlchemy and Pydantic models
```

## Setup and Installation

1. Clone this repository:

```bash
git clone https://github.com/syedaAnusha/FastAPI-library-API-CRUD-example.git
```

2. Create a virtual environment:

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Navigate to the library_api directory and run the application:

```bash
cd library_api
fastapi dev main.py --port 8001
```

The API will be available at `http://127.0.0.1:8001/`

## API Endpoints

| Method | Endpoint           | Description               |
| ------ | ------------------ | ------------------------- |
| POST   | `/books/`          | Create a new book         |
| GET    | `/books/`          | Get all books             |
| GET    | `/books/{book_id}` | Get a specific book by ID |
| PUT    | `/books/{book_id}` | Update a book             |
| DELETE | `/books/{book_id}` | Delete a book             |

## Data Model

Book structure:

```json
{
    "id": int,
    "title": string,
    "author": string,
    "published_year": int
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
