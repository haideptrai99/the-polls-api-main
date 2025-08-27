from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ChoiceCreate(BaseModel):
    """Choice write data model, representing a single choice in a poll"""

    description: str = Field(min_length=1, max_length=100)


class Choice(ChoiceCreate):
    """Choice read model, with an a label and auto-gen uuid"""

    id: UUID = Field(default_factory=uuid4)
    label: int = Field(gt=0, lt=6)


class PollCreate(BaseModel):
    """Poll write data model"""

    title: str = Field(min_length=5, max_length=50)
    options: List[str]
    expires_at: Optional[datetime] = None


class Poll(PollCreate):
    """Poll read data model, with uuid and creation date"""

    id: UUID = Field(default_factory=uuid4)
    options: List[Choice]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
