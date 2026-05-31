"""
Generate a realistic synthetic waste dataset for 7 Kuta Beach zones.
Run: python src/generate_dataset.py
"""
from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from src.utils import (
    ZONES, ZONE_WASTE_MULTIPLIER, DAY_TYPES, WEATHER_CONDITIONS,
    EVENT_TYPES, SEASONS, DATASET_PATH, ensure_dirs,
)

np.random.seed(42)

# ── Bali public holidays (approximate, repeating set) ─────────────────────────
HOLIDAY_DATES = [
    "01-01", "03-03", "03-28", "03-29", "04-10", "04-11",
    "05-01", "05-12", "05-29", "06-01", "06-07", "07-07",
    "07-17", "08-17", "09-27", "10-12", "12-25", "12-31",
]


def _is_holiday(dt: datetime) -> bool:
    return dt.strftime("%m-%d") in HOLIDAY_DATES


def _get_season(dt: datetime) -> str:
    month = dt.month
    if month in (6, 7, 8):
        return "Peak Tourist Season"
    elif month in (11, 12, 1, 2, 3):
        return "Wet Season"
    else:
        return "Dry Season"


def _pick_weather(season: str) -> tuple[str, float]:
    """Return (weather_condition, rainfall_mm) influenced by season."""
    if season == "Wet Season":
        weights = [0.15, 0.25, 0.45, 0.15]
    elif season == "Peak Tourist Season":
        weights = [0.55, 0.25, 0.15, 0.05]
    else:
        weights = [0.45, 0.30, 0.20, 0.05]

    weather = np.random.choice(WEATHER_CONDITIONS, p=weights)
    if weather == "Sunny":
        rain = 0.0
    elif weather == "Cloudy":
        rain = round(np.random.uniform(0, 2), 1)
    elif weather == "Rainy":
        rain = round(np.random.uniform(5, 25), 1)
    else:  # Stormy
        rain = round(np.random.uniform(20, 60), 1)
    return weather, rain


def _pick_event(zone: str, day_type: str, is_holiday: bool) -> str:
    """Higher chance of events in Event Area and on holidays/weekends."""
    base_prob = 0.08
    if zone == "Event Area":
        base_prob = 0.30
    if zone == "Beachwalk Area":
        base_prob += 0.05
    if day_type == "Weekend":
        base_prob += 0.10
    if is_holiday:
        base_prob += 0.15
    if np.random.random() < base_prob:
        return np.random.choice(EVENT_TYPES[1:])  # exclude "None"
    return "None"


def _compute_waste(
    zone: str, is_weekend: bool, is_holiday: bool,
    weather: str, rainfall: float, event: str,
    visitors: int, prev_waste: float, season: str,
    bin_avail: int,
) -> float:
    """Deterministic base + noise formula for waste_volume_kg."""
    # Start from a base value
    base = 400.0

    # Zone multiplier
    base *= ZONE_WASTE_MULTIPLIER[zone]

    # Day type
    if is_weekend:
        base *= 1.30
    if is_holiday:
        base *= 1.45

    # Weather
    if weather == "Rainy":
        base *= 1.15
    elif weather == "Stormy":
        base *= 1.25

    # Event boost
    event_mult = {
        "None": 1.0,
        "Beach Festival": 2.5,
        "Cultural Ceremony": 1.8,
        "Music Concert": 2.8,
        "Sports Event": 2.0,
        "Market Day": 1.6,
    }
    base *= event_mult.get(event, 1.0)

    # Visitor influence (scaled)
    base += visitors * 0.03

    # Season influence
    if season == "Peak Tourist Season":
        base *= 1.25
    elif season == "Wet Season":
        base *= 1.05

    # Bin availability (fewer bins → more overflow waste)
    if bin_avail < 15:
        base *= 1.10

    # Previous-day momentum (autoregressive feel)
    base = 0.7 * base + 0.3 * prev_waste

    # Add noise ±15 %
    noise = np.random.uniform(0.85, 1.15)
    return round(max(base * noise, 50), 1)


def generate_dataset(start_date: str = "2024-01-01", days: int = 365) -> pd.DataFrame:
    """Generate synthetic dataset spanning `days` calendar days x 7 zones."""
    rows: list[dict] = []
    start = datetime.strptime(start_date, "%Y-%m-%d")

    # Track previous waste per zone for autoregressive feature
    prev_waste = {z: np.random.uniform(350, 550) for z in ZONES}

    for d in range(days):
        dt = start + timedelta(days=d)
        dow = dt.weekday()  # 0=Mon … 6=Sun
        is_wknd = dow >= 5
        holiday = _is_holiday(dt)
        day_type = "Public Holiday" if holiday else ("Weekend" if is_wknd else "Weekday")
        season = _get_season(dt)
        weather, rainfall = _pick_weather(season)

        for zone in ZONES:
            event = _pick_event(zone, day_type, holiday)

            # Visitor estimate driven by zone, day type, and events
            vis_base = np.random.randint(800, 2500)
            if zone in ("Beachwalk Area", "Event Area"):
                vis_base = int(vis_base * 1.4)
            if is_wknd:
                vis_base = int(vis_base * 1.3)
            if holiday:
                vis_base = int(vis_base * 1.5)
            if event != "None":
                vis_base = int(vis_base * np.random.uniform(1.5, 2.5))
            visitors = vis_base

            bin_avail = np.random.randint(8, 30)

            waste = _compute_waste(
                zone, is_wknd, holiday, weather, rainfall,
                event, visitors, prev_waste[zone], season, bin_avail,
            )

            rows.append({
                "date": dt.strftime("%Y-%m-%d"),
                "zone": zone,
                "day_of_week": dow,
                "day_type": day_type,
                "is_weekend": int(is_wknd),
                "is_holiday": int(holiday),
                "weather_condition": weather,
                "rainfall_mm": rainfall,
                "event_type": event,
                "estimated_visitors": visitors,
                "season": season,
                "bin_availability": bin_avail,
                "previous_waste_kg": round(prev_waste[zone], 1),
                "waste_volume_kg": waste,
            })

            prev_waste[zone] = waste  # update for next day

    df = pd.DataFrame(rows)
    return df


def main():
    ensure_dirs()
    print("[*] Generating synthetic dataset ...")
    df = generate_dataset()
    df.to_csv(DATASET_PATH, index=False)
    print(f"[OK] Dataset saved to {DATASET_PATH}")
    print(f"     Rows: {len(df):,}  |  Columns: {len(df.columns)}")
    print(f"     Date range: {df['date'].min()} -> {df['date'].max()}")
    print(f"     Zones: {df['zone'].nunique()}")
    print(f"\n[STATS] Waste volume stats:\n{df['waste_volume_kg'].describe().to_string()}")


if __name__ == "__main__":
    main()
