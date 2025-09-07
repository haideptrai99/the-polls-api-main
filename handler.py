from collections.abc import Callable
from typing import Any, cast

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

from app.exceptions.custom_all import (
    BaseCustomException,
    ItemNotFoundException,
    custom_exception_handler,
    generic_exception_handler,
    validation_exception_handler_custom,
)

# ==============================================================================
# PHẦN 3: TẠO VÀ CẤU HÌNH ỨNG DỤNG FASTAPI
# ==============================================================================

app = FastAPI()

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


# ==============================================================================
# PHẦN 4: CÁC ENDPOINTS VÍ DỤ ĐỂ KIỂM THỬ
# ==============================================================================


class Item(BaseModel):
    name: str
    price: float


@app.get("/items/{item_id}")
async def read_item(item_id: int) -> dict[str, int | str] | None:
    """
    Endpoint ví dụ để kiểm thử CustomException.
    """
    if item_id == 42:
        return {"item_id": item_id, "name": "The Answer"}
    # Giả lập không tìm thấy item
    raise ItemNotFoundException(item_id=item_id, location="read_item")


@app.post("/items/")
async def create_item(item: Item) -> Item:
    """
    Endpoint ví dụ để kiểm thử RequestValidationError.
    """
    return item


@app.get("/divide-by-zero")
async def divide_by_zero() -> dict[str, Any]:
    """
    Endpoint ví dụ để kiểm thử generic Exception handler (fallback).
    """
    result = 1 / 0
    return {"result": result}


class Post(BaseModel):
    id: int
    title: str


@app.get("/post/{post_id}")
async def get_post(post_id: int) -> dict[str, int]:
    """
    Endpoint ví dụ để kiểm thử RequestValidationError.
    """
    return {"post_id": post_id}
