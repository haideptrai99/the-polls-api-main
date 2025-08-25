from datetime import datetime, timezone
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Poll(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    options: List[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
