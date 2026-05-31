from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes_analytics import router as analytics_router
from .api.routes_dashboard import router as dashboard_router
from .api.routes_prediction import router as prediction_router
from .core.config import settings
from .core.paths import ensure_project_root_on_path
from .schemas.common import HealthResponse

ensure_project_root_on_path()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FastAPI backend for Kuta WasteSense AI dashboard.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["health"])
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="kuta-wastesense-api",
        version=settings.app_version,
    )


app.include_router(prediction_router)
app.include_router(dashboard_router)
app.include_router(analytics_router)
