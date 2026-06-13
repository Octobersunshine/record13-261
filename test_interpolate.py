import pandas as pd
from resample_service import ResampleService

print("=== 测试1：线性插值（按日补齐缺失数据） ===")
df1 = pd.DataFrame({
    "date": ["2025-01-01", "2025-01-03", "2025-01-06"],
    "value": [10.0, 30.0, 60.0],
})
svc1 = ResampleService(df1, "date", "value")
result1 = svc1.interpolate(freq="D", method="linear")
print(result1)
print()

print("=== 测试2：前向填充（按日补齐缺失数据） ===")
result2 = svc1.interpolate(freq="D", method="ffill")
print(result2)
print()

print("=== 测试3：小时级数据，线性插值 ===")
df3 = pd.DataFrame({
    "ts": ["2025-01-01 00:00", "2025-01-01 04:00", "2025-01-01 06:00"],
    "val": [0.0, 40.0, 60.0],
})
svc3 = ResampleService(df3, "ts", "val")
result3 = svc3.interpolate(freq="h", method="linear")
print(result3)
print()

print("=== 测试4：带时区数据插值 ===")
dates_tz = pd.to_datetime([
    "2025-01-01 00:00",
    "2025-01-03 00:00",
]).tz_localize("Asia/Shanghai")
df4 = pd.DataFrame({
    "date": dates_tz,
    "value": [100.0, 300.0],
})
svc4 = ResampleService(df4, "date", "value")
result4 = svc4.interpolate(freq="D", method="linear")
print(result4)
