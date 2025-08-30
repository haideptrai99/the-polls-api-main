from uuid import UUID

from fastapi import APIRouter

from app.models.Votes import VoteById, VoteByLabel

router = APIRouter()


@router.post("/{poll_id}/id")
def vote_by_id(poll_id: UUID, vote: VoteById) -> dict[str, str]:
    return {"message": "Vote recorded"}


@router.post("/{poll_id}/label")
def vote_by_label(poll_id: UUID, vote: VoteByLabel) -> dict[str, str]:
    return {"message": "Vote recorded"}
