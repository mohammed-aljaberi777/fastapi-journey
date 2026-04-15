from fastapi import APIRouter, HTTPException, status
from typing import List
from beanie import PydanticObjectId

from database.connection import Database
from models.events import Event, EventUpdate

event_router = APIRouter()

event_db = Database(Event)


@event_router.get("/", response_model=List[Event])
async def get_all_events():
    return await event_db.get_all()


@event_router.get("/{id}", response_model=Event)
async def get_event(id: PydanticObjectId):
    event = await event_db.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event


@event_router.post("/new")
async def create_event(event: Event):
    await event_db.save(event)
    return {"message": "Event created successfully"}


@event_router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate):
    updated = await event_db.update(id, body)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return updated


@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId):
    deleted = await event_db.delete(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return {"message": "Event deleted successfully"}