# Bookstore Inventory API

A simple bookstore management REST API built with **FastAPI** and **SQLModel**, backed by **PostgreSQL**. Supports creating, listing, searching, and updating books, plus inventory tracking metrics.

## Tech Stack

| Tool | Purpose |
|---|---|
| FastAPI | Web framework |
| SQLModel | ORM + Pydantic validation combined |
| PostgreSQL | Database (via Docker) |
| psycopg2-binary | PostgreSQL driver |
| python-dotenv | Loads config from `.env` |
| Docker Compose | Runs PostgreSQL locally |

## Project Structure
bookstore-api/
├── main.py                   # FastAPI app and all endpoints
├── models/
│   ├── init.py
│   └── book.py                # Book, BookCreate, BookUpdate models
├── database/
│   ├── init.py
│   └── session.py             # DB engine and session dependency
├── .env                      # DATABASE_URL (not committed to git)
├── docker-compose.yml        # PostgreSQL container config
└── venv/                     # Virtual environment (not committed to git)


## Setup

### 1. Clone and enter the project

```powershell
cd bookstore-api
2. Create and activate a virtual environment
PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
3. Install dependencies
PowerShell
pip install fastapi uvicorn sqlmodel psycopg2-binary alembic python-dotenv
4. Configure environment variables
Create a .env file in the project root:

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/bookstore_db
5. Start PostgreSQL
PowerShell
docker compose up -d
Verify it's running:

PowerShell
docker ps
6. Run the API
PowerShell
uvicorn main:app --reload
The API will be available at http://localhost:8000, with interactive docs at http://localhost:8000/docs.

API Endpoints
Method	Endpoint	Description
GET	/	Welcome message
POST	/books	Create a new book
GET	/books	List all books (supports skip, limit, author, available, max_price filters)
GET	/books/search	Search books by title or author substrings
GET	/books/{book_id}	Get a single book by ID
PATCH	/books/{book_id}	Update a book (partial updates supported)
DELETE	/books/{book_id}	Delete a book entry entirely
Example: Create a book
JSON
POST /books
{
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "isbn": "9780261102217",
  "published_year": 1937,
  "price": 14.99,
  "stock": 15,
  "available": true
}
Example: Search books
GET /books/search?q=Tolkien
GET /books/search?q=Hobbit
Example: Update a book
JSON
PATCH /books/1
{
  "price": 16.99,
  "stock": 12
}
Data Models
Book

id (integer), title (string), author (string), isbn (unique string), published_year (integer), price (float), stock (integer), available (boolean), created_at (datetime), updated_at (datetime)

Notes
Route ordering matters: /books/search is declared before /books/{book_id} so FastAPI doesn't try to interpret "search" as a book ID numerical path parameter.

BookUpdate uses exclude_unset=True so PATCH requests only modify the fields explicitly sent, protecting untouched attributes.

To reset the database schema after model changes: docker compose down -v && docker compose up -d.

Author
C027-01-0860/2024