from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.models.Votes import Vote, VoteById, VoteByLabel, Voter
from app.services import utils

router = APIRouter()


@router.post("/{poll_id}/id")
def vote_by_id(poll_id: UUID, vote: VoteById) -> dict[str, Any]:
    poll = utils.get_poll(poll_id)

    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")

    if not poll.is_active():
        raise HTTPException(status_code=400, detail="The poll has expired")

    if utils.get_vote(poll_id, vote.voter.email):
        raise HTTPException(status_code=400, detail="Already voted")

    if vote.choice_id not in [choice.id for choice in poll.options]:
        raise HTTPException(status_code=400, detail="Invalid choice id specified")

    vote_model = Vote(
        poll_id=poll_id,
        choice_id=vote.choice_id,
        voter=Voter(**vote.voter.model_dump()),
    )

    utils.save_vote(poll_id, vote=vote_model)

    return {"message": "Vote recorded", "vote": vote_model}


@router.post("/{poll_id}/label")
def vote_by_label(poll_id: UUID, vote: VoteByLabel) -> dict[str, Any]:
    poll = utils.get_poll(poll_id)

    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")

    if not poll.is_active():
        raise HTTPException(status_code=400, detail="The poll has expired")

    if utils.get_vote(poll_id, vote.voter.email):
        raise HTTPException(status_code=400, detail="Already voted")

    choice_id = utils.get_choice_id_by_label(poll_id, vote.choice_label)

    if not choice_id:
        raise HTTPException(status_code=400, detail="Invalid choice label provided.")

    vote_model = Vote(
        poll_id=poll_id,
        choice_id=choice_id,
        voter=Voter(**vote.voter.model_dump()),
    )

    utils.save_vote(poll_id, vote=vote_model)

    return {"message": "Vote recorded", "vote": vote_model}
