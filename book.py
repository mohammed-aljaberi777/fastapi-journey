from fastapi import APIRouter,HTTPException,Request
from typing import List 
import asyncio
from models import Book 
from fastapi import status 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


book_router = APIRouter()

templates = Jinja2Templates(directory="templates")

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
  

@book_router.post("/books/",status_code=status.HTTP_201_CREATED)
async def add_book(book:Book):
  for b in books:
     if b.id == book.id:
        raise HTTPException(status_code=400,detail="Book exists")


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


@book_router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "books": books
    })


@book_router.get("/book/{book_id}", response_class=HTMLResponse)
async def get_book_page(request: Request, book_id: int):
    for book in books:
        if book.id == book_id:
            return templates.TemplateResponse("book.html", {
                "request": request,
                "book": book
            })

    raise HTTPException(status_code=404, detail="Book not found")
    
      






