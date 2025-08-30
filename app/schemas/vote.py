from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel


class VoteResponse(BaseModel):
    poll_id: UUID
    choice_id: UUID
    voter: dict[str, Any]


class VoteWithMessage(BaseModel):
    message: str
    vote: VoteResponse
