from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from ..core.paths import ensure_project_root_on_path

ensure_project_root_on_path()

from src.utils import EVENT_TYPES, SEASONS, WEATHER_CONDITIONS, ZONES


DayType = Literal["Weekday", "Weekend", "Public Holiday"]
WeatherCondition = Literal["Sunny", "Cloudy", "Rainy", "Stormy"]
Season = Literal["Dry Season", "Wet Season", "Peak Tourist Season"]
RiskLevel = Literal["Low", "Medium", "High"]


class PredictionRequest(BaseModel):
    zone: str
    prediction_date: date
    day_type: DayType
    weather_condition: WeatherCondition
    rainfall_mm: float = Field(ge=0, le=100)
    event_type: str
    estimated_visitors: int = Field(ge=0, le=100000)
    season: Season
    bin_availability: int = Field(ge=0, le=100)
    previous_waste_kg: float = Field(ge=0, le=20000)

    @field_validator("zone")
    @classmethod
    def validate_zone(cls, value: str) -> str:
        if value not in ZONES:
            raise ValueError(f"zone must be one of: {', '.join(ZONES)}")
        return value

    @field_validator("event_type")
    @classmethod
    def validate_event_type(cls, value: str) -> str:
        if value not in EVENT_TYPES:
            raise ValueError(f"event_type must be one of: {', '.join(EVENT_TYPES)}")
        return value

    @field_validator("season")
    @classmethod
    def validate_season(cls, value: str) -> str:
        if value not in SEASONS:
            raise ValueError(f"season must be one of: {', '.join(SEASONS)}")
        return value

    @field_validator("weather_condition")
    @classmethod
    def validate_weather(cls, value: str) -> str:
        if value not in WEATHER_CONDITIONS:
            raise ValueError(f"weather_condition must be one of: {', '.join(WEATHER_CONDITIONS)}")
        return value


class SimulationRequest(BaseModel):
    zone: str
    prediction_date: date
    weather_condition: WeatherCondition
    rainfall_mm: float = Field(ge=0, le=100)
    holiday_status: bool = False
    event_type: str = "None"
    estimated_visitors: int = Field(ge=0, le=100000)
    season: Season
    bin_availability: int = Field(default=18, ge=0, le=100)
    previous_waste_kg: float = Field(default=500.0, ge=0, le=20000)

    @field_validator("zone")
    @classmethod
    def validate_zone(cls, value: str) -> str:
        if value not in ZONES:
            raise ValueError(f"zone must be one of: {', '.join(ZONES)}")
        return value

    @field_validator("event_type")
    @classmethod
    def validate_event_type(cls, value: str) -> str:
        if value not in EVENT_TYPES:
            raise ValueError(f"event_type must be one of: {', '.join(EVENT_TYPES)}")
        return value


class PredictionResult(BaseModel):
    predicted_waste_kg: float
    predicted_waste_tons: float
    risk_level: RiskLevel


class RecommendationResult(BaseModel):
    recommended_staff: int
    recommended_bins: int
    recommended_trucks: int
    collection_schedule: str


class PredictionResponse(BaseModel):
    input: PredictionRequest
    prediction: PredictionResult
    recommendation: RecommendationResult
    summary: str


class SimulationResponse(BaseModel):
    scenario_id: str
    prediction: PredictionResult
    recommendation: RecommendationResult
    insight: str
