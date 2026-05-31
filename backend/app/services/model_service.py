from __future__ import annotations

from functools import lru_cache

import joblib
import pandas as pd

from ..core.paths import MODEL_PATH, ensure_project_root_on_path
from ..schemas.prediction import PredictionRequest

ensure_project_root_on_path()

from src.utils import FEATURE_COLS


@lru_cache(maxsize=1)
def get_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


def build_feature_frame(request: PredictionRequest) -> pd.DataFrame:
    is_weekend = int(request.day_type == "Weekend")
    is_holiday = int(request.day_type == "Public Holiday")

    input_df = pd.DataFrame([
        {
            "zone": request.zone,
            "day_of_week": request.prediction_date.weekday(),
            "is_weekend": is_weekend,
            "is_holiday": is_holiday,
            "weather_condition": request.weather_condition,
            "rainfall_mm": request.rainfall_mm,
            "event_type": request.event_type,
            "estimated_visitors": request.estimated_visitors,
            "season": request.season,
            "bin_availability": request.bin_availability,
            "previous_waste_kg": request.previous_waste_kg,
        }
    ])

    return input_df[FEATURE_COLS]


def predict_waste(request: PredictionRequest) -> float:
    model = get_model()
    features = build_feature_frame(request)
    predicted_kg = float(model.predict(features)[0])
    return max(predicted_kg, 0.0)
