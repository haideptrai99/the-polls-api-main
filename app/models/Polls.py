from datetime import UTC, datetime
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from pydantic import (
    BaseModel,
    Field,
    FieldSerializationInfo,
    computed_field,
    field_serializer,
    field_validator,
)

from app.models.Choice import Choice
from app.utils import timezones

VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")


class PollCreate(BaseModel):
    """Poll write data model"""

    title: str = Field(min_length=5, max_length=50)
    options: list[str]
    expires_at: datetime | None = Field(default_factory=lambda: datetime.now(UTC))

    # "expires_at": "2026-09-03 21:30:00"
    # --------------------------------------------------------------------------
    # ✨ FIX: Thêm validator để tự động gán múi giờ cho input
    # --------------------------------------------------------------------------
    # @field_validator("expires_at")
    # @classmethod
    # def localize_naive_datetime(cls, v: datetime | None) -> datetime | None:
    #     """
    #     Nếu datetime được nhập vào là "naive" (không có múi giờ),
    #     hàm này sẽ tự động gán múi giờ Việt Nam (Asia/Ho_Chi_Minh) cho nó.
    #     """
    #     if v is not None and v.tzinfo is None:
    #         # Gán múi giờ VN cho datetime naive
    #         return v.replace(tzinfo=VN_TZ)
    #     # Nếu đã có múi giờ hoặc là None thì giữ nguyên
    #     return v

    # --------------------------------------------------------------------------

    @computed_field
    def full_name(self) -> str:
        return "fullname:haideptrai"

    @field_serializer("expires_at")
    def serialize_expires_at(
        self, v: datetime | None, _info: FieldSerializationInfo
    ) -> str | None:
        return timezones.format_vn_time(v)

    @field_validator("options")
    @classmethod
    def validate_options(cls, v: list[str]) -> list[str]:
        if len(v) < 2 or len(v) > 5:
            # raise ValueError("A poll must contain between 2 and 5 choices")
            raise HTTPException(
                status_code=400, detail="A poll must contain between 2 and 5 choices"
            )
        return v

    def create_poll(self) -> "Poll":
        """
        Create a new Poll instance with auto-incrementing labels for
        Choices, e.g. 1, 2, 3

        This will be used in the POST /polls/create endpoint
        """
        choices = [
            Choice(description=desc, label=index + 1)
            for index, desc in enumerate(self.options)
        ]

        if self.expires_at is not None and self.expires_at < datetime.now(UTC):
            raise HTTPException(
                status_code=400, detail="A poll's expiration must be in the future"
            )

        return Poll(title=self.title, options=choices, expires_at=self.expires_at)


class Poll(PollCreate):
    """Poll read data model, with uuid and creation date"""

    id: UUID = Field(default_factory=uuid4)
    options: list[Choice]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def is_active(self) -> bool:
        if self.expires_at is None:
            return True

        return datetime.now(UTC) < self.expires_at
