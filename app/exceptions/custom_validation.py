from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# --- BẮT ĐẦU PHẦN TỐI ƯU ---

# 1. TẠO "TỪ ĐIỂN LỖI" TẬP TRUNG
# Key: một tuple có dạng (*location, error_type)
# Value: chuỗi thông báo tùy chỉnh
CUSTOM_VALIDATION_MESSAGES = {
    # Lỗi cho poll_id trong router /polls/{poll_id}
    (
        "path",
        "poll_id",
        "uuid_parsing",
    ): "ID của poll không hợp lệ. Vui lòng cung cấp một UUID chính xác.",
    # Thêm các lỗi khác ở đây một cách dễ dàng
    # Ví dụ: lỗi cho một tham số query 'page'
    ("query", "page", "int_parsing"): "Số trang phải là một số nguyên.",
    # Ví dụ: lỗi cho một trường trong body request
    (
        "body",
        "user_profile",
        "email",
        "email_parsing",
    ): "Địa chỉ email không đúng định dạng.",
    # Ví dụ: lỗi giá trị bị thiếu
    ("body", "title", "missing"): "Trường 'title' là bắt buộc.",
}


# 2. VIẾT LẠI EXCEPTION HANDLER ĐỂ SỬ DỤNG TỪ ĐIỂN
async def validation_exception_handler(
    _request: Request, exc: Exception
) -> JSONResponse:
    """
    Xử lý lỗi xác thực bằng cách tra cứu trong từ điển lỗi tập trung.
    """
    if isinstance(exc, RequestValidationError):
        # Lặp qua danh sách các lỗi mà Pydantic trả về
        for error in exc.errors():
            # Tạo khóa để tra cứu từ thông tin lỗi
            # error['loc'] là một tuple, ví dụ ('path', 'poll_id')
            # error['type'] là chuỗi, ví dụ 'uuid_parsing'
            error_key = (*error["loc"], error["type"])

            # Tra cứu trong từ điển. Dùng .get() để tránh lỗi nếu không tìm thấy
            custom_message = CUSTOM_VALIDATION_MESSAGES.get(error_key)

            # Nếu tìm thấy thông báo tùy chỉnh, trả về ngay lập tức
            if custom_message:
                return JSONResponse(
                    status_code=422,
                    content={"detail": custom_message},
                )

    # Nếu không có lỗi nào được ánh xạ trong từ điển, trả về một lỗi chung
    return JSONResponse(
        status_code=422,
        content={"detail": "Dữ liệu đầu vào không hợp lệ. Vui lòng kiểm tra lại."},
    )
