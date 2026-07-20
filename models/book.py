from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

# Base validation settings for books
class BookBase(SQLModel):
    title: str = Field(index=True, min_length=1, max_length=150)
    author: str = Field(index=True, min_length=1, max_length=100)
    isbn: str = Field(index=True, unique=True, min_length=10, max_length=13)
    published_year: int = Field(ge=1000, le=2026) # 2026 is the current year
    price: float = Field(gt=0)
    stock: int = Field(ge=0, default=0)
    available: bool = Field(default=True)

# 1. Main Database Model (table=True)
class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# 2. BookCreate model (Everything required when making a new book)
class BookCreate(BookBase):
    pass  # Inherits all the required fields from BookBase!

# 3. BookUpdate model (For updating an existing book - everything is optional)
class BookUpdate(SQLModel):
    title: Optional[str] = Field(None, min_length=1, max_length=150)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, min_length=10, max_length=13)
    published_year: Optional[int] = Field(None, ge=1000, le=2026)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    available: Optional[bool] = None