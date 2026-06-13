import pandas as pd
from resample_service import ResampleService

print("=== 测试1：无时区数据（保持原有行为） ===")
df1 = pd.DataFrame({
    "date": ["2025-01-01 00:00", "2025-01-01 12:00", "2025-01-02 00:00"],
    "value": [10, 20, 30],
})
svc1 = ResampleService(df1, "date", "value")
print(svc1.resample("D", "sum"))
print()

print("=== 测试2：带时区数据（北京时间 Asia/Shanghai） ===")
dates_tz = pd.to_datetime([
    "2025-01-01 07:00",
    "2025-01-01 08:00",
    "2025-01-01 23:00",
    "2025-01-02 07:59",
    "2025-01-02 08:00",
]).tz_localize("Asia/Shanghai")

df2 = pd.DataFrame({
    "date": dates_tz,
    "value": [1, 10, 100, 1000, 10000],
})
svc2 = ResampleService(df2, "date", "value")
result = svc2.resample("D", "sum")
print(result)
print()

print("说明（UTC 视角）：")
print("  北京时间 01-01 07:00 → UTC 12-31 23:00 → 归入 12-31")
print("  北京时间 01-01 08:00 → UTC 01-01 00:00 → 归入 01-01")
print("  北京时间 01-02 07:59 → UTC 01-01 23:59 → 归入 01-01")
print("  北京时间 01-02 08:00 → UTC 01-02 00:00 → 归入 01-02")
print()
print(f"预期：12-31 = 1, 01-01 = 10+100+1000=1110, 01-02 = 10000")
print(f"实际：{result['value'].tolist()}")
