from collections.abc import Callable
from typing import cast

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

from app.api import danger, polls, votes
from app.exceptions.custom_all import (
    BaseCustomException,
    custom_exception_handler,
    generic_exception_handler,
    validation_exception_handler_custom,
)

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

# app.add_exception_handler(
#     RequestValidationError, custom_validation.validation_exception_handler
# )

# ==============================================================================
# PHẦN 3: TẠO VÀ CẤU HÌNH ỨNG DỤNG FASTAPI
# ==============================================================================

# --- Đăng ký các exception handlers ---
# Thứ tự đăng ký quan trọng: từ cụ thể nhất đến chung nhất.
app.add_exception_handler(
    BaseCustomException,
    cast(Callable[[Request, Exception], Response], custom_exception_handler),
)
app.add_exception_handler(
    RequestValidationError,
    cast(
        Callable[[Request, Exception], Response], validation_exception_handler_custom
    ),  # <--- ÁP DỤNG Ở ĐÂY
)
app.add_exception_handler(
    Exception, generic_exception_handler
)  # Đăng ký handler chung cuối cùng

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
