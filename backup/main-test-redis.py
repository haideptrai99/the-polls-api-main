from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel
from upstash_redis import Redis

from app.models.Polls import PollCreate
from config import get_settings

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
    return {"detail": "Poll sucesss created", "poll_id": new_poll.id, "poll": new_poll}


class RedisResponse(BaseModel):
    id: str
    name: str | None = None


settings = get_settings()
if settings.UPSTASH_REDIS_URL is None or settings.UPSTASH_REDIS_TOKEN is None:
    raise RuntimeError(
        "UPSTASH_REDIS_URL and UPSTASH_REDIS_TOKEN must be set in .env or environment"
    )

redis_client = Redis(url=settings.UPSTASH_REDIS_URL, token=settings.UPSTASH_REDIS_TOKEN)


@app.get("/redis/get/{redis_id}", tags=["throwaway"], response_model=RedisResponse)
def get_redis(redis_id: str) -> RedisResponse:
    value = redis_client.get(redis_id)
    if isinstance(value, bytes):
        value = value.decode()
    return RedisResponse(id=redis_id, name=value)


class SaveResponse(BaseModel):
    status: str


@app.post("/redis/save", tags=["throwaway"], response_model=SaveResponse)
def save_redis(redis_id: str, name: str) -> SaveResponse:
    redis_client.set(redis_id, name)
    return SaveResponse(status="success")
