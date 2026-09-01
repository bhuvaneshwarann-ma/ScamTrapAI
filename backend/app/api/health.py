"""
ScamTrap AI — Health Check Endpoint

Provides ``GET /health`` for infrastructure probes (load balancers, Docker
health checks, monitoring). Returns application status, version, and uptime.
"""

import time
from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.core.config import settings

router = APIRouter(tags=["system"])

# Captured once at import time — used to compute uptime
_START_TIME = time.monotonic()
_START_TIMESTAMP = datetime.now(timezone.utc).isoformat()


class HealthResponse(BaseModel):
    """Health check response schema."""

    status: str = "ok"
    app_name: str
    version: str
    uptime_seconds: float
    started_at: str
    timestamp: str
    llm_provider: str
    embedding_provider: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Application health check.

    Returns basic system status, version info, and uptime.
    Used by Docker health checks, load balancers, and monitoring dashboards.
    """
    return HealthResponse(
        status="ok",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        uptime_seconds=round(time.monotonic() - _START_TIME, 2),
        started_at=_START_TIMESTAMP,
        timestamp=datetime.now(timezone.utc).isoformat(),
        llm_provider=settings.LLM_PROVIDER,
        embedding_provider=settings.EMBEDDING_PROVIDER,
    )
