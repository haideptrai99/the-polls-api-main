from typing import Annotated

from fastapi import Depends, FastAPI, Path
from fastapi.params import Query
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    name: str
    age: int
    email: str


@app.post("/")
def create_user(user: User) -> User:
    """
    Endpoint check create user validate age integer.
    """
    user_data = user
    return user_data


@app.get("/check/{item_id}")
def get_item(item_id: int) -> int:
    return item_id


@app.get("/items/{item_id}")
async def get_items(
    item_id: Annotated[
        int,
        Path(
            gt=0,  # gt: Greater Than (lớn hơn 0)
            title="The ID of the item to get",
            description="ID của bài viết cần lấy. Phải là một số nguyên dương và không lớn hơn 1000.",
        ),
    ],
    q: Annotated[str | None, Query(alias="item-query")] = None,
) -> dict[str, int | str]:  # Sửa type hint ở đây để chính xác hơn
    # 💡 FIX: Khai báo tường minh kiểu dữ liệu cho `results`.
    # Điều này báo cho trình phân tích kiểu biết rằng dictionary này
    # có thể chứa cả `int` (từ item_id) và `str` (từ q).
    results: dict[str, int | str] = {"item_id": item_id}

    # Nếu tham số truy vấn `q` tồn tại, thêm nó vào kết quả.
    if q:
        # Giờ đây, việc cập nhật với một giá trị chuỗi là hoàn toàn hợp lệ
        # theo như kiểu dữ liệu đã khai báo.
        # results.update({"q": q})

        # Một cách viết khác, rõ ràng hơn khi chỉ thêm một cặp key-value:
        results["q"] = q

    return results


@app.get("/post/{post_id}")
async def get_post(
    post_id: Annotated[
        int,
        Path(
            title="Post ID",
            description="ID của bài viết cần lấy. Phải là một số nguyên dương và không lớn hơn 1000.",
            gt=0,  # gt: Greater Than (lớn hơn 0)
            le=1000,  # le: Less than or Equal to (nhỏ hơn hoặc bằng 1000)
        ),
    ],
) -> dict[str, int]:
    """
    Endpoint lấy thông tin bài viết theo ID đã được validate.
    """
    # Tại thời điểm này, bạn có thể chắc chắn rằng post_id đã hợp lệ (1 <= post_id <= 1000)
    return {"post_id": post_id}


# 1. Đây là hàm dependency của chúng ta
async def common_parameters(skip: int = 0, limit: int = 100) -> dict[str, int]:
    """
    Hàm này xử lý các tham số truy vấn chung cho việc phân trang.
    Nó nhận `skip` và `limit`, sau đó trả về một dictionary.
    """
    return {"skip": skip, "limit": limit}


# 2. Sử dụng dependency trong path operation function
@app.get("/depend/")
async def read_depend(
    commons: Annotated[dict[str, int], Depends(common_parameters)],
) -> dict[str, str]:
    """
    Endpoint để lấy danh sách các item.
    Tham số `commons` sẽ nhận giá trị trả về từ `common_parameters`.
    """
    # Bây giờ bạn có thể sử dụng `commons` như một dictionary thông thường
    return {
        "message": f"Fetching {commons['limit']} items, skipping {commons['skip']} items."
    }


@app.get("/depend-users/")
async def read_depend_users(
    commons: Annotated[dict[str, int], Depends(common_parameters)],
) -> dict[str, str]:
    """
    Một endpoint khác cũng sử dụng lại dependency `common_parameters`.
    Điều này cho thấy khả năng tái sử dụng tuyệt vời.
    """
    return {
        "message": f"Fetching {commons['limit']} users, skipping {commons['skip']} users."
    }
