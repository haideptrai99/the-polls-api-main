from fastapi import FastAPI
from pydantic import BaseModel

from app.api import polls

app = FastAPI()

app.include_router(polls.router, prefix="/polls", tags=["polls"])


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
