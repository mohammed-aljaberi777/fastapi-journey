
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from .models import PollCreate, VoteRequest
from .storage import store

load_dotenv()  # reads .env into os.environ

APP_NAME = os.getenv("APP_NAME", "Real-Time Polling App")

app = FastAPI(title=APP_NAME)


@app.get("/", tags=["meta"])
def root():
    return {"app": APP_NAME, "status": "ok"}


# ---------------------------------------------------------------------------
# REST endpoints
# ---------------------------------------------------------------------------

@app.post("/polls", status_code=201, tags=["polls"])
def create_poll(payload: PollCreate):
    """Create a new poll with a question and 2-10 options."""
    return store.create_poll(payload.question, payload.options)


@app.get("/polls", tags=["polls"])
def list_polls():
    """Return all polls currently in memory."""
    return store.list_polls()


@app.get("/polls/{poll_id}", tags=["polls"])
def get_poll(poll_id: str):
    """Return a single poll by id."""
    poll = store.get_poll(poll_id)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll


@app.post("/polls/{poll_id}/vote", tags=["polls"])
async def vote_rest(poll_id: str, payload: VoteRequest):
    """
    Cast a vote via REST. This is the fallback path for clients that
    can't or don't want to open a WebSocket. WebSocket clients on the
    same poll WILL still receive the broadcast (added in Task 2).
    """
    poll = await store.add_vote(poll_id, payload.option_index)
    if poll is None:
        raise HTTPException(
            status_code=404,
            detail="Poll not found or option_index out of range",
        )
    return poll


@app.delete("/polls/{poll_id}", status_code=204, tags=["polls"])
def delete_poll(poll_id: str):
    """Delete a poll by id."""
    if not store.delete_poll(poll_id):
        raise HTTPException(status_code=404, detail="Poll not found")
    return None
