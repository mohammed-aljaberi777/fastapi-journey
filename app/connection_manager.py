

import asyncio
from typing import Dict, List, Set
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        # poll_id -> set of WebSocket objects
        self._rooms: Dict[str, Set[WebSocket]] = {}
        # Lock to keep the rooms dict consistent under concurrency.
        self._lock = asyncio.Lock()

    async def connect(self, poll_id: str, websocket: WebSocket) -> None:
        """Accept the handshake and add the socket to the room."""
        await websocket.accept()
        async with self._lock:
            self._rooms.setdefault(poll_id, set()).add(websocket)

    async def disconnect(self, poll_id: str, websocket: WebSocket) -> None:
        """Remove the socket from the room. Safe if it's already gone."""
        async with self._lock:
            room = self._rooms.get(poll_id)
            if room:
                room.discard(websocket)
                if not room:
                    del self._rooms[poll_id]

    async def broadcast(self, poll_id: str, message: dict) -> None:
        """Send a JSON message to every client in this poll's room."""
        async with self._lock:
            connections: List[WebSocket] = list(self._rooms.get(poll_id, set()))

        dead: List[WebSocket] = []
        for ws in connections:
            try:
                await ws.send_json(message)
            except Exception:
                # Client disappeared mid-send — mark for cleanup.
                dead.append(ws)

        for ws in dead:
            await self.disconnect(poll_id, ws)

    def count(self, poll_id: str) -> int:
        return len(self._rooms.get(poll_id, set()))


# One shared manager for the whole app.
manager = ConnectionManager()