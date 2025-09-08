from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Lớp cấu hình ứng dụng, tự động đọc các biến từ môi trường
    hoặc tệp .env.
    """

    # Map tới biến môi trường: UPSTASH_REDIS_URL
    UPSTASH_REDIS_URL: str | None = Field(default=None)
    # Map tới biến môi trường: UPSTASH_REDIS_TOKEN
    UPSTASH_REDIS_TOKEN: str | None = Field(default=None)

    # Cấu hình để đọc từ tệp .env ở thư mục gốc của dự án
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # extra='ignore' # Bỏ qua các biến môi trường thừa nếu có
    )


# Hàm khởi tạo và trả về settings, có thể tái sử dụng
def get_settings() -> Settings:
    try:
        # Khởi tạo settings, Pydantic sẽ tự động đọc từ .env
        settings = Settings()
        return settings
    except ValidationError as e:
        print(
            "🔴 LỖI: Không thể tải cấu hình. Vui lòng kiểm tra các biến môi trường hoặc tệp .env."
        )
        print("Chi tiết lỗi từ Pydantic:")
        # In ra thông báo lỗi rõ ràng từ Pydantic
        print(e)
        # Thoát chương trình với mã lỗi
        exit(1)


# Phần code chính để chạy và kiểm tra
if __name__ == "__main__":
    print("Đang cố gắng tải cấu hình...")
    # Lấy đối tượng settings đã được validate
    app_settings = get_settings()

    print("\n✅ Cấu hình đã được tải thành công!")

    # In ra các giá trị đã được tải để xác nhận
    # model_dump() chuyển đổi đối tượng Pydantic thành dictionary
    # Lưu ý: Không bao giờ in token ra log trong môi trường production!
    # Ở đây chúng ta chỉ in để gỡ lỗi.
    print("Giá trị cấu hình:")
    # Chuyển đổi HttpUrl thành chuỗi để in ra
    dumped_settings = app_settings.model_dump()
    dumped_settings["UPSTASH_REDIS_URL"] = str(dumped_settings["UPSTASH_REDIS_URL"])
    print(dumped_settings)
