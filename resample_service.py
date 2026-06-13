import pandas as pd
from typing import Literal, Union

FREQ_MAP = {
    "D": "D",
    "day": "D",
    "daily": "D",
    "W": "W-SUN",
    "week": "W-SUN",
    "weekly": "W-SUN",
    "M": "ME",
    "month": "ME",
    "monthly": "ME",
}

AGG_MAP = {
    "sum": "sum",
    "mean": "mean",
}

INTERP_MAP = {
    "linear": "linear",
    "ffill": "ffill",
    "forward": "ffill",
}


class ResampleService:
    def __init__(self, df: pd.DataFrame, time_col: str, value_col: str):
        if time_col not in df.columns:
            raise ValueError(f"时间列 '{time_col}' 不存在")
        if value_col not in df.columns:
            raise ValueError(f"值列 '{value_col}' 不存在")

        self._df = df.copy()
        self._df[time_col] = pd.to_datetime(self._df[time_col])
        self._df = self._df.sort_values(time_col).set_index(time_col)
        self._time_col = time_col
        self._value_col = value_col

    def interpolate(
        self,
        freq: str,
        method: Literal["linear", "ffill", "forward"] = "linear",
    ) -> pd.DataFrame:
        method_code = INTERP_MAP.get(method)
        if method_code is None:
            raise ValueError(f"不支持的插值方式 '{method}'，可选: {list(INTERP_MAP.keys())}")

        df = self._df
        if df.index.tz is not None:
            df = df.tz_convert("UTC")

        full_index = pd.date_range(start=df.index.min(), end=df.index.max(), freq=freq)
        reindexed = df.reindex(full_index)

        if method_code == "linear":
            interpolated = reindexed.interpolate(method="time")
        else:
            interpolated = reindexed.ffill()

        interpolated.index.name = df.index.name or "time"
        interpolated = interpolated.reset_index()
        interpolated.columns = [self._time_col, self._value_col]
        return interpolated

    def resample(
        self,
        freq: Literal["D", "W", "M", "day", "week", "month", "daily", "weekly", "monthly"],
        agg: Literal["sum", "mean"] = "sum",
    ) -> pd.DataFrame:
        freq_code = FREQ_MAP.get(freq)
        if freq_code is None:
            raise ValueError(f"不支持的频率 '{freq}'，可选: {list(FREQ_MAP.keys())}")

        agg_method = AGG_MAP.get(agg)
        if agg_method is None:
            raise ValueError(f"不支持的聚合方式 '{agg}'，可选: {list(AGG_MAP.keys())}")

        df = self._df
        if df.index.tz is not None:
            df = df.tz_convert("UTC")

        resampled = df.resample(freq_code)
        result = getattr(resampled, agg_method)()
        result = result.reset_index()
        result.columns = [df.index.name or "time", df.columns[0]]
        return result
