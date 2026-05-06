

import asyncio
import uuid
from typing import Dict, List, Optional


class PollStore:
    def __init__(self) -> None:
        # poll_id -> { question, options: [{text, votes}], ... }
        self._polls: Dict[str, dict] = {}
        # One lock per poll keeps concurrent votes on different polls fast.
        self._locks: Dict[str, asyncio.Lock] = {}

    def _lock_for(self, poll_id: str) -> asyncio.Lock:
        if poll_id not in self._locks:
            self._locks[poll_id] = asyncio.Lock()
        return self._locks[poll_id]

    def create_poll(self, question: str, options: List[str]) -> dict:
        poll_id = str(uuid.uuid4())
        poll = {
            "id": poll_id,
            "question": question,
            "options": [
                {"index": i, "text": text, "votes": 0}
                for i, text in enumerate(options)
            ],
        }
        self._polls[poll_id] = poll
        return self._serialize(poll)

    def list_polls(self) -> List[dict]:
        return [self._serialize(p) for p in self._polls.values()]

    def get_poll(self, poll_id: str) -> Optional[dict]:
        poll = self._polls.get(poll_id)
        return self._serialize(poll) if poll else None

    def delete_poll(self, poll_id: str) -> bool:
        if poll_id in self._polls:
            del self._polls[poll_id]
            self._locks.pop(poll_id, None)
            return True
        return False

    async def add_vote(self, poll_id: str, option_index: int) -> Optional[dict]:
        """Atomically increment a vote count and return the updated poll."""
        poll = self._polls.get(poll_id)
        if poll is None:
            return None
        if option_index < 0 or option_index >= len(poll["options"]):
            return None

        async with self._lock_for(poll_id):
            poll["options"][option_index]["votes"] += 1
            return self._serialize(poll)

    @staticmethod
    def _serialize(poll: dict) -> dict:
        total = sum(opt["votes"] for opt in poll["options"])
        return {
            "id": poll["id"],
            "question": poll["question"],
            "options": [dict(opt) for opt in poll["options"]],
            "total_votes": total,
        }


# Single shared store for the whole app.
store = PollStore()
