from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.models.Polls import Poll, PollCreate
from app.services import utils

router = APIRouter()


# @app.post("/polls/create")
@router.post("/create")
def create_poll(poll: PollCreate) -> dict[str, Any]:
    new_poll = poll.create_poll()
    utils.save_poll(new_poll)
    return {"detail": "Poll sucesss created", "poll_id": new_poll.id, "poll": new_poll}


# @app.get("/polls/{poll_id}", response_model=Poll)
@router.get("/{poll_id}")
def get_poll(poll_id: UUID) -> Poll:
    poll = utils.get_poll(poll_id)
    if not poll:
        raise HTTPException(status_code=400, detail="A poll id not correct")
    return poll
