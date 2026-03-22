from fastapi import FastAPI
from book import book_router

app = FastAPI()

@app.get("/")
async def welcome():
    return {"message": "Welcome to the Library API"}

app.include_router(book_router)