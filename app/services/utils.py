from uuid import UUID

from upstash_redis import Redis

from app.models.Polls import Poll
from config import get_settings

settings = get_settings()
if settings.UPSTASH_REDIS_URL is None or settings.UPSTASH_REDIS_TOKEN is None:
    raise RuntimeError(
        "UPSTASH_REDIS_URL and UPSTASH_REDIS_TOKEN must be set in .env or environment"
    )

redis_client = Redis(url=settings.UPSTASH_REDIS_URL, token=settings.UPSTASH_REDIS_TOKEN)


def save_poll(poll: Poll) -> None:
    poll_json = poll.model_dump_json()
    redis_client.set(f"poll:{poll.id}", poll_json)


def get_poll(poll_id: UUID) -> Poll | None:
    poll_json = redis_client.get(f"poll:{poll_id}")
    if poll_json:
        return Poll.model_validate_json(poll_json)
    return None
