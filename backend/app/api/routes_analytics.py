from __future__ import annotations

from fastapi import APIRouter

from ..schemas.analytics import AnalyticsOverviewResponse
from ..services.analytics_service import get_analytics_overview

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview", response_model=AnalyticsOverviewResponse)
def analytics_overview() -> dict:
    return get_analytics_overview()
