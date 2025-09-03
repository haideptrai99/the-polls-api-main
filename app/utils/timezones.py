from datetime import datetime
from zoneinfo import ZoneInfo

UTC_TZ = ZoneInfo("UTC")
VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")


def localize_vn_datetime(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC_TZ)
    return dt.astimezone(VN_TZ)


def format_vn_time(v: datetime | None) -> str | None:
    if v is None:
        return None
    # vn_time = v.astimezone(VN_TZ)
    return v.strftime("%d-%m-%Y %H:%M:%S")
