from __future__ import annotations

from pydantic import BaseModel

from .common import DateRange


class TopRiskZone(BaseModel):
    zone: str
    average_waste_kg: float


class AnalyticsOverviewResponse(BaseModel):
    total_records: int
    date_range: DateRange
    zones_count: int
    average_waste_kg: float
    max_waste_kg: float
    top_risk_zones: list[TopRiskZone]
