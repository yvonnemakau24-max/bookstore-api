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

| File / Folder | Purpose |
|---|---|
| main.py | FastAPI app and all endpoints |
| models/ | Data models folder |
| models/__init__.py | Package initializer |
| models/book.py | Book, BookCreate, and BookUpdate models |
| database/ | Database configuration folder |
| database/__init__.py | Package initializer |
| database/session.py | DB engine and session dependency |
| .env | DATABASE_URL configuration |
| docker-compose.yml | PostgreSQL container config |
| venv/ | Virtual environment |
## Setup

### 1. Clone and enter the project

```powershell
cd bookstore-api
2. Create and activate a virtual environment

python -m venv venv
.\venv\Scripts\Activate.ps1
3. Install dependenciesPowerShellpip install fastapi uvicorn 

sqlmodel psycopg2-binary alembic python-dotenv
4. Configure environment variablesCreate a .env file in the project root:
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/bookstore_db

5. Start PostgreSQL
PowerShell
docker compose up -d

Verify it is running:
PowerShell
docker ps

6. Run the API
PowerShell
uvicorn main:app --reload

The API will be available at http://localhost:8000, with interactive docs at http://localhost:8000/docs.API 
## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| POST | `/books` | Create a new book |
| GET | `/books` | List all books (supports `skip`, `limit`, `author`, `available`, `max_price` filters) |
| GET | `/books/search` | Search books by `title` or `author` substrings |
| GET | `/books/{book_id}` | Get a single book by ID |
| PATCH | `/books/{book_id}` | Update a book (partial updates supported) |
{
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "isbn": "9780261102217",
  "published_year": 1937,
  "price": 14.99,
  "stock": 15,
  "available": true
}
Example: 
Search books
GET /books/search?q=Tolkien
GET /books/search?q=Hobbit

Example: Update a bookJSONPATCH /books/1
{
  "price": 16.99,
  "stock": 12
}
Data Models
Book
id, title, author, isbn (unique), published_year, price, stock, available, created_at, updated_at
Notes
   -Route ordering matters: /books/search is declared before /books/{book_id} so FastAPI does not try to interpret "search" as a book ID.

    -BookUpdate uses exclude_unset=True so PATCH requests only modify the fields explicitly sent, not all fields.

    -To reset the database schema after model changes: docker compose down -v && docker compose up -d.
    
AuthorC027-01-0860/2024