

from typing import List
from pydantic import BaseModel, Field


class PollCreate(BaseModel):
    """Body sent by the client when creating a new poll."""
    question: str = Field(..., min_length=1, max_length=200)
    options: List[str] = Field(..., min_length=2, max_length=10)


class VoteRequest(BaseModel):
    """Body sent by the client when casting a vote via REST."""
    option_index: int = Field(..., ge=0)


class PollOption(BaseModel):
    """A single option inside a poll, including its current vote count."""
    index: int
    text: str
    votes: int


class Poll(BaseModel):
    """A full poll, returned by the API."""
    id: str
    question: str
    options: List[PollOption]
    total_votes: int
