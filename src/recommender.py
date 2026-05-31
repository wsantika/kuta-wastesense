"""
Rule-based operational recommendation engine.
Translates predicted waste volume into actionable recommendations.
"""

import math
from src.utils import (
    STAFF_CAPACITY_KG, BIN_CAPACITY_KG, TRUCK_CAPACITY_KG,
    RISK_LOW_MAX, RISK_MEDIUM_MAX,
)


def get_risk_level(predicted_kg: float) -> str:
    """Classify risk level from predicted waste volume."""
    if predicted_kg < RISK_LOW_MAX:
        return "Low"
    elif predicted_kg <= RISK_MEDIUM_MAX:
        return "Medium"
    else:
        return "High"


def get_recommendations(predicted_kg: float) -> dict:
    """
    Return a full recommendation dict:
      - risk_level
      - recommended_staff
      - recommended_bins
      - recommended_trucks
      - collection_schedule
    """
    risk = get_risk_level(predicted_kg)

    rec_staff = math.ceil(predicted_kg / STAFF_CAPACITY_KG)
    rec_bins = math.ceil(predicted_kg / BIN_CAPACITY_KG)
    rec_trucks = math.ceil(predicted_kg / TRUCK_CAPACITY_KG)

    if risk == "Low":
        schedule = "1x per day (morning)"
    elif risk == "Medium":
        schedule = "2x per day (morning & evening)"
    else:
        schedule = "3x per day (before event, during event, after event)"

    return {
        "predicted_waste_kg": round(predicted_kg, 1),
        "risk_level": risk,
        "recommended_staff": rec_staff,
        "recommended_bins": rec_bins,
        "recommended_trucks": rec_trucks,
        "collection_schedule": schedule,
    }


def generate_executive_summary(
    zone: str,
    predicted_kg: float,
    weather: str,
    event: str,
    visitors: int,
    rec: dict,
) -> str:
    """Generate a plain-English executive summary paragraph."""
    risk = rec["risk_level"]

    # Build reason fragments
    reasons: list[str] = []
    if visitors > 3000:
        reasons.append("high visitor density")
    if weather in ("Rainy", "Stormy"):
        reasons.append(f"{weather.lower()} weather conditions")
    if event != "None":
        reasons.append(f"scheduled {event.lower()} activity")

    reason_str = (
        " due to " + ", ".join(reasons[:-1]) + f", and {reasons[-1]}"
        if len(reasons) > 1
        else (" due to " + reasons[0] if reasons else "")
    )

    summary = (
        f"**{zone}** is predicted to generate **{risk.lower()} waste volume "
        f"({predicted_kg:,.0f} kg)**{reason_str}. "
        f"The system recommends deploying **{rec['recommended_staff']} sanitation staff**, "
        f"providing **{rec['recommended_bins']} waste bins**, "
        f"dispatching **{rec['recommended_trucks']} collection truck(s)**, "
        f"and following a **{rec['collection_schedule'].lower()}** collection schedule."
    )

    return summary
