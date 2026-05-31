from __future__ import annotations

from ..core.paths import ensure_project_root_on_path
from ..schemas.prediction import RecommendationResult

ensure_project_root_on_path()

from src.recommender import generate_executive_summary, get_recommendations


def build_recommendation(predicted_kg: float) -> RecommendationResult:
    rec = get_recommendations(predicted_kg)
    return RecommendationResult(
        recommended_staff=rec["recommended_staff"],
        recommended_bins=rec["recommended_bins"],
        recommended_trucks=rec["recommended_trucks"],
        collection_schedule=rec["collection_schedule"],
    )


def build_summary(
    zone: str,
    predicted_kg: float,
    weather: str,
    event: str,
    visitors: int,
    recommendation: RecommendationResult,
) -> str:
    rec_dict = {
        "risk_level": get_recommendations(predicted_kg)["risk_level"],
        "recommended_staff": recommendation.recommended_staff,
        "recommended_bins": recommendation.recommended_bins,
        "recommended_trucks": recommendation.recommended_trucks,
        "collection_schedule": recommendation.collection_schedule,
    }
    return generate_executive_summary(zone, predicted_kg, weather, event, visitors, rec_dict)
