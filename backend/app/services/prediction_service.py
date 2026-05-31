from __future__ import annotations

from datetime import date

from ..core.paths import ensure_project_root_on_path
from ..schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
    PredictionResult,
    SimulationRequest,
    SimulationResponse,
)
from .model_service import predict_waste
from .recommendation_service import build_recommendation, build_summary

ensure_project_root_on_path()

from src.recommender import get_recommendations


def _build_prediction_result(predicted_kg: float) -> PredictionResult:
    rec = get_recommendations(predicted_kg)
    return PredictionResult(
        predicted_waste_kg=round(predicted_kg, 1),
        predicted_waste_tons=round(predicted_kg / 1000, 2),
        risk_level=rec["risk_level"],
    )


def run_prediction(request: PredictionRequest) -> PredictionResponse:
    predicted_kg = predict_waste(request)
    prediction = _build_prediction_result(predicted_kg)
    recommendation = build_recommendation(predicted_kg)
    summary = build_summary(
        request.zone,
        predicted_kg,
        request.weather_condition,
        request.event_type,
        request.estimated_visitors,
        recommendation,
    )

    return PredictionResponse(
        input=request,
        prediction=prediction,
        recommendation=recommendation,
        summary=summary,
    )


def _day_type_from_simulation(prediction_date: date, holiday_status: bool) -> str:
    if holiday_status:
        return "Public Holiday"
    return "Weekend" if prediction_date.weekday() >= 5 else "Weekday"


def run_simulation(request: SimulationRequest) -> SimulationResponse:
    prediction_request = PredictionRequest(
        zone=request.zone,
        prediction_date=request.prediction_date,
        day_type=_day_type_from_simulation(request.prediction_date, request.holiday_status),
        weather_condition=request.weather_condition,
        rainfall_mm=request.rainfall_mm,
        event_type=request.event_type,
        estimated_visitors=request.estimated_visitors,
        season=request.season,
        bin_availability=request.bin_availability,
        previous_waste_kg=request.previous_waste_kg,
    )
    response = run_prediction(prediction_request)
    scenario_id = f"sim_{request.prediction_date.strftime('%Y%m%d')}_{request.zone.lower().replace(' ', '_')}"

    return SimulationResponse(
        scenario_id=scenario_id,
        prediction=response.prediction,
        recommendation=response.recommendation,
        insight=response.summary,
    )
