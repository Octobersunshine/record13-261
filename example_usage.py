import pandas as pd
from resample_service import ResampleService

dates = pd.date_range("2025-01-01", periods=90, freq="D")
df = pd.DataFrame({
    "date": dates,
    "value": range(90),
})

svc = ResampleService(df, time_col="date", value_col="value")

daily_sum = svc.resample("D", "sum")
weekly_mean = svc.resample("W", "mean")
monthly_sum = svc.resample("M", "sum")

print("=== 按日聚合 (sum) ===")
print(daily_sum.head(10))
print()

print("=== 按周聚合 (mean) ===")
print(weekly_mean)
print()

print("=== 按月聚合 (sum) ===")
print(monthly_sum)
