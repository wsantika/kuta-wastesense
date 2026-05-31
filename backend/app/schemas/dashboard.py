from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from .prediction import RiskLevel


class RiskZoneCounts(BaseModel):
    low: int
    medium: int
    high: int


class RiskZonePercentages(BaseModel):
    low: float
    medium: float
    high: float


class DashboardSummaryResponse(BaseModel):
    predicted_waste_tons: float
    predicted_window_hours: int
    waste_delta_percent: float
    risk_zones: RiskZoneCounts
    risk_zone_percentages: RiskZonePercentages
    generated_at: datetime


class DashboardZone(BaseModel):
    zone_id: str
    zone_name: str
    risk_level: RiskLevel
    predicted_waste_kg: float
    latitude: float
    longitude: float
    color: str


class DashboardZonesResponse(BaseModel):
    zones: list[DashboardZone]


class VisitorDensityPoint(BaseModel):
    hour: int
    visitors: int


class RainfallForecastPoint(BaseModel):
    hour: int
    rainfall_mm: float


class EventImpactPoint(BaseModel):
    hour: int
    impact_score: float


class HistoricalWastePoint(BaseModel):
    date: str
    waste_tons: float


class DashboardTrendsResponse(BaseModel):
    visitor_density: list[VisitorDensityPoint]
    rainfall_forecast: list[RainfallForecastPoint]
    event_impact: list[EventImpactPoint]
    historical_waste: list[HistoricalWastePoint]


class RecommendationMetric(BaseModel):
    required: int
    delta_vs_normal: int


class CollectionScheduleSummary(BaseModel):
    label: str
    time_range: str


class DashboardRecommendationsResponse(BaseModel):
    sanitation_staff: RecommendationMetric
    additional_bins: RecommendationMetric
    collection_trucks: RecommendationMetric
    collection_schedule: CollectionScheduleSummary
