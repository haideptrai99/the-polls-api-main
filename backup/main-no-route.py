from typing import Any
from uuid import UUID

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.models.Polls import Poll, PollCreate
from app.services import utils

app = FastAPI()


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


@app.post("/polls/create")
def create_poll(poll: PollCreate) -> dict[str, Any]:
    new_poll = poll.create_poll()
    utils.save_poll(new_poll)
    return {"detail": "Poll sucesss created", "poll_id": new_poll.id, "poll": new_poll}


@app.get("/polls/{poll_id}", response_model=Poll)
def get_poll(poll_id: UUID) -> Poll:
    poll = utils.get_poll(poll_id)
    if not poll:
        raise HTTPException(status_code=400, detail="A poll id not correct")
    return poll
