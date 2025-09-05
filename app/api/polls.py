from enum import Enum
from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.Polls import Poll, PollCreate
from app.models.Results import PollResults
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


class PollStatus(Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    ALL = "all"


class PollsListResponse(BaseModel):
    count: int
    polls: list[Poll]


@router.get("/")
def get_polls(status: PollStatus = PollStatus.ACTIVE) -> PollsListResponse:
    polls = utils.get_all_polls()

    if not polls:
        raise HTTPException(status_code=404, detail="No polls were found")

    if status == PollStatus.ACTIVE:
        filtered_polls = [poll for poll in polls if poll.is_active()]
    elif status == PollStatus.EXPIRED:
        filtered_polls = [poll for poll in polls if not poll.is_active()]
    else:  # PollStatus.ALL
        filtered_polls = polls

    return PollsListResponse(count=len(filtered_polls), polls=filtered_polls)


@router.get("/{poll_id}/results")
def get_results(poll_id: UUID) -> PollResults | None:
    # results = utils.get_vote_count(poll_id)
    # return {"results": results}

    return utils.get_poll_results(poll_id)
