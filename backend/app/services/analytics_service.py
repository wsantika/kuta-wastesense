from __future__ import annotations

from functools import lru_cache

import pandas as pd

from ..core.paths import DATASET_PATH


@lru_cache(maxsize=1)
def get_dataset() -> pd.DataFrame:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset file not found: {DATASET_PATH}")
    return pd.read_csv(DATASET_PATH, parse_dates=["date"])


def get_analytics_overview() -> dict:
    df = get_dataset()
    zone_avg = (
        df.groupby("zone")["waste_volume_kg"]
        .mean()
        .sort_values(ascending=False)
        .head(3)
        .reset_index()
    )

    return {
        "total_records": int(len(df)),
        "date_range": {
            "start": df["date"].min().date().isoformat(),
            "end": df["date"].max().date().isoformat(),
        },
        "zones_count": int(df["zone"].nunique()),
        "average_waste_kg": round(float(df["waste_volume_kg"].mean()), 1),
        "max_waste_kg": round(float(df["waste_volume_kg"].max()), 1),
        "top_risk_zones": [
            {"zone": row["zone"], "average_waste_kg": round(float(row["waste_volume_kg"]), 1)}
            for _, row in zone_avg.iterrows()
        ],
    }


def get_historical_waste_trends(days: int = 30) -> list[dict]:
    df = get_dataset()
    daily = (
        df.sort_values("date")
        .groupby("date")["waste_volume_kg"]
        .sum()
        .reset_index()
        .tail(days)
    )

    return [
        {
            "date": row["date"].date().isoformat(),
            "waste_tons": round(float(row["waste_volume_kg"]) / 1000, 2),
        }
        for _, row in daily.iterrows()
    ]
