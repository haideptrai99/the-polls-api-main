from datetime import datetime
from zoneinfo import ZoneInfo  # Sử dụng thư viện chuẩn của Python (từ 3.9+)

# 1. Xác định múi giờ Việt Nam
vietnam_timezone = ZoneInfo("Asia/Ho_Chi_Minh")

# 2. Lấy thời gian hiện tại theo múi giờ Việt Nam
current_time_vn = datetime.now(vietnam_timezone)

# 3. Định dạng theo chuỗi "d/m/y H:M:S"
formatted_time = current_time_vn.strftime("%d/%m/%Y %H:%M:%S")

# In kết quả
print(f"Thời gian gốc (datetime object): {current_time_vn}")
print(f"Thời gian đã định dạng: {formatted_time}")
print(type(formatted_time))
