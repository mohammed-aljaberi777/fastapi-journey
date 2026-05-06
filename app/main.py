

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect

from .models import PollCreate, VoteRequest
from .storage import store
from .connection_manager import manager

load_dotenv()

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
    Cast a vote via REST. This is the fallback path. It still broadcasts
    the update to any connected WebSocket clients on this poll, so REST
    voters and WebSocket voters see the same live counts.
    """
    poll = await store.add_vote(poll_id, payload.option_index)
    if poll is None:
        raise HTTPException(
            status_code=404,
            detail="Poll not found or option_index out of range",
        )
    await manager.broadcast(poll_id, {"type": "update", "poll": poll})
    return poll


@app.delete("/polls/{poll_id}", status_code=204, tags=["polls"])
def delete_poll(poll_id: str):
    """Delete a poll by id."""
    if not store.delete_poll(poll_id):
        raise HTTPException(status_code=404, detail="Poll not found")
    return None


# ---------------------------------------------------------------------------
# WebSocket endpoint
# ---------------------------------------------------------------------------

@app.websocket("/ws/polls/{poll_id}")
async def ws_poll(websocket: WebSocket, poll_id: str):
    """
    Real-time channel for a single poll.

    Client -> Server messages (JSON):
      {"type": "vote", "option_index": <int>}
      {"type": "ping"}

    Server -> Client messages (JSON):
      {"type": "snapshot", "poll": <Poll>}    # sent once on connect
      {"type": "update",   "poll": <Poll>}    # sent to ALL on every vote
      {"type": "pong"}                        # reply to ping
      {"type": "error",    "message": <str>}
    """
    # Reject the connection if the poll doesn't exist.
    poll = store.get_poll(poll_id)
    if poll is None:
        await websocket.accept()
        await websocket.send_json({"type": "error", "message": "Poll not found"})
        await websocket.close()
        return

    await manager.connect(poll_id, websocket)

    try:
        # Send the current state immediately so the new client is in sync.
        await websocket.send_json({"type": "snapshot", "poll": poll})

        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            if msg_type == "vote":
                option_index = data.get("option_index")
                if not isinstance(option_index, int):
                    await websocket.send_json(
                        {"type": "error", "message": "option_index must be int"}
                    )
                    continue

                updated = await store.add_vote(poll_id, option_index)
                if updated is None:
                    await websocket.send_json(
                        {"type": "error", "message": "Invalid option_index or poll deleted"}
                    )
                    continue

                # Push the new state to EVERY client in this room.
                await manager.broadcast(poll_id, {"type": "update", "poll": updated})

            elif msg_type == "ping":
                await websocket.send_json({"type": "pong"})

            else:
                await websocket.send_json(
                    {"type": "error", "message": f"unknown type: {msg_type!r}"}
                )

    except WebSocketDisconnect:
        # Normal client disconnect — just clean up.
        await manager.disconnect(poll_id, websocket)
    except Exception:
        # Any other failure: also clean up so we don't leak sockets.
        await manager.disconnect(poll_id, websocket)