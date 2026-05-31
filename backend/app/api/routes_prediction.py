from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from ..schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
    SimulationRequest,
    SimulationResponse,
)
from ..services.prediction_service import run_prediction, run_simulation

router = APIRouter(tags=["prediction"])


@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    try:
        return run_prediction(request)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc


@router.post("/simulate", response_model=SimulationResponse)
def simulate(request: SimulationRequest) -> SimulationResponse:
    try:
        return run_simulation(request)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
