from uuid import UUID

from pydantic import BaseModel


class Result(BaseModel):
    description: str
    vote_count: int


class PollResults(BaseModel):
    id: UUID
    title: str
    total_votes: int
    results: list[Result]
