from fastapi import APIRouter,HTTPException
from typing import List 
import asyncio
from models import Book 

book_router = APIRouter()

books: List[Book] = []

@book_router.get("/books/")
async def get_books():
  await asyncio.sleep(1)
  return books

@book_router.get("/books/{book_id}")
async def get_book(book_id:int):
  for book in books:
    if book.id == book_id:
      return book
  raise HTTPException(status_code=404, detail="Book not found")
  

@book_router.post("/books/")
async def add_book(book:Book):
  books.append(book)
  return {"message": "Book added successfully", "book": book}


@book_router.put("/books/{book_id}")
async def update_book(book_id: int,updated_book:Book):
  for index, book in enumerate(books):
    if book.id == book_id:
      books[index] = updated_book
      return {"message": "Book updated", "book": updated_book}
  raise HTTPException(status_code=404, detail="Book not found")


@book_router.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book.id == book_id:
            deleted = books.pop(index)
            return {"message": "Book deleted", "book": deleted}

    raise HTTPException(status_code=404, detail="Book not found")
    
      






