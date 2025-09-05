from fastapi import FastAPI
from pydantic import BaseModel

from app.api import danger, polls, votes

app = FastAPI(
    title="Polls API",
    description="A simple API to create and vote on polls",
    version="0.1",
    openapi_tags=[
        {
            "name": "polls",
            "description": "Operations related to creating and viewing polls",
        },
        {
            "name": "danger",
            "description": "Operations that lead to irreversible data loss",
        },
        {
            "name": "votes",
            "description": "Operations related to casting votes",
        },
    ],
)

app.include_router(polls.router, prefix="/polls", tags=["polls"])
app.include_router(danger.router, prefix="/polls", tags=["danger"])
app.include_router(votes.router, prefix="/vote", tags=["votes"])


class Message(BaseModel):
    message: str


@app.get(
    "/",
    response_model=Message,
    summary="summary hello world",
    description="mô tả hàm",
)
def read_root() -> Message:
    return Message(message="Hello, World!")
