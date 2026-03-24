from fastapi import APIRouter,HTTPException,Request

import asyncio
from models import Book 
from fastapi import status 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import managed_db


book_router = APIRouter()

templates = Jinja2Templates(directory="templates")






@book_router.get("/books/")
async def get_books():
  await asyncio.sleep(1)
  with managed_db() as db:
        return db.get_all()

@book_router.get("/books/{book_id}")
async def get_book(book_id:int):
   with managed_db() as db:
        book = db.get(book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book


@book_router.post("/books/",status_code=status.HTTP_201_CREATED)
async def add_book(book:Book):
   with managed_db() as db:
        new_id = db.create(book)
        created_book = db.get(new_id)
        return {"message": "Book added successfully", "book": created_book}


 

@book_router.put("/books/{book_id}")
async def update_book(book_id: int,updated_book:Book):
   with managed_db() as db:
        existing_book = db.get(book_id)
        if existing_book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        
        updated = db.update(book_id, updated_book)
        return {"message": "Book updated", "book": updated}



@book_router.delete("/books/{book_id}")
async def delete_book(book_id: int):
    with managed_db() as db:
        book = db.get(book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        db.delete(book_id)
        return {"message": "Book deleted", "book": book}


@book_router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    with managed_db() as db:
        return templates.TemplateResponse("home.html", {
            "request": request,
            "books": db.get_all()
        })


@book_router.get("/book/{book_id}", response_class=HTMLResponse)
async def get_book_page(request: Request, book_id: int):
    with managed_db() as db:
        book = db.get(book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        return templates.TemplateResponse("book.html", {
            "request": request,
            "book": book
        })






