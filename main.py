# main.py
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlmodel import Session, select, or_
from typing import List, Optional
from datetime import datetime

from database.session import get_session, create_db_and_tables
from models.book import Book, BookCreate, BookUpdate

app = FastAPI(title="Bookstore Inventory API", version="1.0.0")

# Initialize database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ------------------------------------------------------------
# BOOK CRUD ENDPOINTS
# ------------------------------------------------------------

@app.post("/books", response_model=Book, status_code=201)
def create_book(book: BookCreate, session: Session = Depends(get_session)):
    """Create a new book in the inventory"""
    # Check if ISBN is already in use
    existing_book = session.exec(select(Book).where(Book.isbn == book.isbn)).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="A book with this ISBN already exists")
    
    db_book = Book(**book.dict())
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@app.get("/books", response_model=List[Book])
def list_books(
    skip: int = 0,
    limit: int = 10,
    author: Optional[str] = None,
    available: Optional[bool] = None,
    max_price: Optional[float] = None,
    session: Session = Depends(get_session)
):
    """List all books with optional filters"""
    query = select(Book)
    
    if author:
        query = query.where(Book.author.ilike(f"%{author}%"))
    if available is not None:
        query = query.where(Book.available == available)
    if max_price is not None:
        query = query.where(Book.price <= max_price)
        
    return session.exec(query.offset(skip).limit(limit)).all()


@app.get("/books/search", response_model=List[Book])
def search_books(q: str = Query(..., min_length=1), session: Session = Depends(get_session)):
    """Search books by title or author"""
    query = select(Book).where(
        or_(
            Book.title.ilike(f"%{q}%"),
            Book.author.ilike(f"%{q}%")
        )
    )
    return session.exec(query).all()


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, session: Session = Depends(get_session)):
    """Get a specific book by its ID"""
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.patch("/books/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    session: Session = Depends(get_session)
):
    """Partially update an existing book"""
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Exclude unset values to only update provided fields
    update_data = book_update.dict(exclude_unset=True)
    
    # Validation block: Check if updating ISBN violates unique constraint
    if "isbn" in update_data and update_data["isbn"] != db_book.isbn:
        isbn_conflict = session.exec(select(Book).where(Book.isbn == update_data["isbn"])).first()
        if isbn_conflict:
            raise HTTPException(status_code=400, detail="ISBN already assigned to another book")

    for key, value in update_data.items():
        setattr(db_book, key, value)
        
    db_book.updated_at = datetime.utcnow()
    
    session.commit()
    session.refresh(db_book)
    return db_book


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    """Delete a book from the inventory"""
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    session.delete(book)
    session.commit()
    return None
