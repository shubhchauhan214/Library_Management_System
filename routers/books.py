from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Book, User
from pydantic import BaseModel
from starlette import status

from routers.auth import get_current_user

router = APIRouter()


class BookCreate(BaseModel):
    title: str
    author: str


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    user_id: int

    class Config:
        from_attributes = True


@router.get("/books/", status_code=status.HTTP_200_OK, response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@router.get("/books/{book_id}", status_code=status.HTTP_200_OK, response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/books/", status_code=status.HTTP_201_CREATED, response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_book = Book(title=book.title, author=book.author, user_id=current_user.id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_book.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this book")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}
