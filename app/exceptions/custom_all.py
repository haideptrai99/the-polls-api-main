import logging
from abc import ABC, abstractmethod

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from rich.logging import RichHandler

# --- Cấu hình Logging (Nên thực hiện ở cấp ứng dụng) ---
# Cấu hình logging cơ bản. Trong dự án thực tế, bạn có thể dùng file cấu hình (dictConfig).
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     handlers=[logging.StreamHandler()],
# )
logging.basicConfig(
    level="INFO",
    format="%(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[RichHandler(rich_tracebacks=True)],  # Kích hoạt traceback đẹp
)

logger = logging.getLogger("rich")
# logger = logging.getLogger(__name__)


# ==============================================================================
# PHẦN 1: ĐỊNH NGHĨA CÁC CUSTOM EXCEPTIONS
# ==============================================================================


class BaseCustomException(Exception, ABC):
    """
    Lớp cơ sở trừu tượng cho tất cả các exception tùy chỉnh.
    Kế thừa từ `Exception` để có thể được raise và except.
    """

    status_code: int = 500

    @property
    @abstractmethod
    def message(self) -> str:
        """Thông báo lỗi trả về cho client."""
        pass

    @property
    @abstractmethod
    def trace(self) -> str:
        """Thông tin chi tiết về lỗi để ghi log, không trả về cho client."""
        pass


class ItemNotFoundException(BaseCustomException):
    """
    Ví dụ một exception cụ thể khi không tìm thấy tài nguyên.
    """

    status_code = 404

    def __init__(self, item_id: int, location: str, exc: Exception | None = None):
        self.item_id = item_id
        self.location = location
        self.exc = exc

    @property
    def message(self) -> str:
        return f"Item with ID {self.item_id} was not found."

    @property
    def trace(self) -> str:
        base_trace = f"ItemNotFoundException raised in '{self.location}' for item_id: {self.item_id}."
        if self.exc:
            return f"{base_trace} Original exception: {self.exc}"
        return base_trace


# ==============================================================================
# PHẦN 2: ĐỊNH NGHĨA CÁC EXCEPTION HANDLERS
# ==============================================================================


async def custom_exception_handler(
    _request: Request, exc: BaseCustomException
) -> JSONResponse:
    """
    Handler dành riêng cho các exception kế thừa từ BaseCustomException.
    """
    logger.error(exc.trace)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handler để định dạng lại lỗi validation của Pydantic cho dễ đọc hơn.
    """
    # Lấy thông tin lỗi chi tiết từ Pydantic
    errors = []
    for error in exc.errors():
        errors.append(
            {
                "location": " -> ".join(map(str, error["loc"])),
                "message": error["msg"],
                "type": error["type"],
            }
        )

    logger.warning(f"Request validation failed: {errors}")
    return JSONResponse(
        status_code=422,  # Unprocessable Entity
        content={"detail": "Validation Error", "errors": errors},
    )


# Tìm đến hàm này trong code của bạn
async def validation_exception_handler_custom(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    # Lấy ra lỗi đầu tiên để làm thông báo
    # Bạn có thể tùy chỉnh logic này tùy ý
    first_error = exc.errors()[0]
    error_location = " -> ".join(map(str, first_error["loc"]))
    custom_message = f"Invalid value for '{error_location}'. {first_error['msg']}."

    logger.warning(
        f"Request validation failed: {exc.errors()}"
    )  # Vẫn log chi tiết để debug

    return JSONResponse(
        status_code=422,
        # Chỉ trả về một thông điệp đơn giản
        content={"detail": custom_message},
    )


async def generic_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    """
    Handler chung để bắt tất cả các lỗi không mong muốn (fallback).
    Đây là chốt chặn cuối cùng để tránh server bị crash.
    """
    logger.critical(f"An unhandled exception occurred: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred. Please try again later."
        },
    )
