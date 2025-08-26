from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Choice(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    description: str = Field(min_length=1, max_length=100)
    label: int = Field(gt=0, lt=6)
