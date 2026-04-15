from fastapi import FastAPI
from database.connection import Settings
from routes.events import event_router
from routes.users import user_router

app = FastAPI()


@app.on_event("startup")
async def start_db():
    settings = Settings()
    await settings.initialize_database()


app.include_router(event_router, prefix="/event")
app.include_router(user_router, prefix="/user")


@app.get("/")
async def root():
    return {"message": "API is running"}