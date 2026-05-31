from __future__ import annotations

from datetime import datetime
from math import ceil

from ..core.paths import ensure_project_root_on_path
from .analytics_service import get_dataset, get_historical_waste_trends

ensure_project_root_on_path()

from src.recommender import get_risk_level
from src.utils import ZONES


ZONE_COORDINATES = {
    "Beachwalk Area": {"lat": -8.7169, "lng": 115.1686},
    "Main Beach Gate": {"lat": -8.7182, "lng": 115.1681},
    "Food Vendor Area": {"lat": -8.7190, "lng": 115.1679},
    "Parking Area": {"lat": -8.7200, "lng": 115.1695},
    "Hotel Front Area": {"lat": -8.7158, "lng": 115.1690},
    "Event Area": {"lat": -8.7212, "lng": 115.1674},
    "Legian-side Beach Zone": {"lat": -8.7108, "lng": 115.1676},
}

RISK_COLORS = {
    "Low": "#22C55E",
    "Medium": "#F59E0B",
    "High": "#EF4444",
}


def _risk_key(risk_level: str) -> str:
    return risk_level.lower()


def _latest_zone_predictions() -> list[dict]:
    df = get_dataset()
    latest_date = df["date"].max()
    latest = df[df["date"] == latest_date]

    rows = []
    for idx, zone in enumerate(ZONES, start=1):
        zone_rows = latest[latest["zone"] == zone]
        if zone_rows.empty:
            predicted_kg = float(df[df["zone"] == zone]["waste_volume_kg"].mean())
        else:
            predicted_kg = float(zone_rows.iloc[0]["waste_volume_kg"])
        risk = get_risk_level(predicted_kg)
        coords = ZONE_COORDINATES[zone]
        rows.append(
            {
                "zone_id": f"Z-{idx:02d}",
                "zone_name": zone,
                "risk_level": risk,
                "predicted_waste_kg": round(predicted_kg, 1),
                "latitude": coords["lat"],
                "longitude": coords["lng"],
                "color": RISK_COLORS[risk],
            }
        )
    return rows


def get_dashboard_summary() -> dict:
    zones = _latest_zone_predictions()
    total_kg = sum(zone["predicted_waste_kg"] for zone in zones)
    counts = {"low": 0, "medium": 0, "high": 0}
    for zone in zones:
        counts[_risk_key(zone["risk_level"])] += 1

    total_zones = max(len(zones), 1)
    percentages = {key: round(value / total_zones * 100, 1) for key, value in counts.items()}

    df = get_dataset()
    daily = df.groupby("date")["waste_volume_kg"].sum().sort_index()
    if len(daily) >= 2:
        previous_total = float(daily.iloc[-2])
        waste_delta = ((total_kg - previous_total) / previous_total * 100) if previous_total else 0.0
    else:
        waste_delta = 0.0

    return {
        "predicted_waste_tons": round(total_kg / 1000, 2),
        "predicted_window_hours": 48,
        "waste_delta_percent": round(waste_delta, 1),
        "risk_zones": counts,
        "risk_zone_percentages": percentages,
        "generated_at": datetime.now(),
    }


def get_dashboard_zones() -> dict:
    return {"zones": _latest_zone_predictions()}


def get_dashboard_trends(days: int = 30) -> dict:
    return {
        "visitor_density": [
            {"hour": 0, "visitors": 16000},
            {"hour": 12, "visitors": 22000},
            {"hour": 24, "visitors": 42600},
            {"hour": 36, "visitors": 31000},
            {"hour": 48, "visitors": 35000},
        ],
        "rainfall_forecast": [
            {"hour": 0, "rainfall_mm": 12.8},
            {"hour": 12, "rainfall_mm": 8.2},
            {"hour": 24, "rainfall_mm": 4.6},
            {"hour": 36, "rainfall_mm": 10.3},
            {"hour": 48, "rainfall_mm": 7.4},
        ],
        "event_impact": [
            {"hour": 0, "impact_score": 35},
            {"hour": 12, "impact_score": 52},
            {"hour": 24, "impact_score": 75},
            {"hour": 36, "impact_score": 68},
            {"hour": 48, "impact_score": 59},
        ],
        "historical_waste": get_historical_waste_trends(days),
    }


def get_dashboard_recommendations() -> dict:
    summary = get_dashboard_summary()
    predicted_kg = summary["predicted_waste_tons"] * 1000

    return {
        "sanitation_staff": {
            "required": max(ceil(predicted_kg / 300), 1),
            "delta_vs_normal": 12,
        },
        "additional_bins": {
            "required": max(ceil(predicted_kg / 150), 1),
            "delta_vs_normal": 15,
        },
        "collection_trucks": {
            "required": max(ceil(predicted_kg / 1500), 1),
            "delta_vs_normal": 2,
        },
        "collection_schedule": {
            "label": "Every 2 Hours",
            "time_range": "06:00 AM - 10:00 PM",
        },
    }
