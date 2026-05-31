from __future__ import annotations

from fastapi import APIRouter, Query

from ..schemas.dashboard import (
    DashboardRecommendationsResponse,
    DashboardSummaryResponse,
    DashboardTrendsResponse,
    DashboardZonesResponse,
)
from ..services.dashboard_service import (
    get_dashboard_recommendations,
    get_dashboard_summary,
    get_dashboard_trends,
    get_dashboard_zones,
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummaryResponse)
def dashboard_summary() -> dict:
    return get_dashboard_summary()


@router.get("/zones", response_model=DashboardZonesResponse)
def dashboard_zones() -> dict:
    return get_dashboard_zones()


@router.get("/trends", response_model=DashboardTrendsResponse)
def dashboard_trends(days: int = Query(default=30, ge=1, le=365)) -> dict:
    return get_dashboard_trends(days)


@router.get("/recommendations", response_model=DashboardRecommendationsResponse)
def dashboard_recommendations() -> dict:
    return get_dashboard_recommendations()
