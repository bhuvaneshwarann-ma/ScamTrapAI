"""
ScamTrap AI — FastAPI Application Factory

Creates and configures the FastAPI application with:
- CORS middleware (configurable origins)
- Request ID middleware (UUID per request for tracing)
- Structured error handling (JSON error responses)
- Structured JSON logging with PII redaction
- Health endpoint
- Startup/shutdown lifecycle hooks
"""

import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from backend.app.core.config import settings
from backend.app.core.logging import setup_logging, get_logger
from backend.app.api.health import router as health_router
from backend.app.api.auth import router as auth_router
from backend.app.api.incidents import router as incidents_router
from backend.app.api.campaigns import router as campaigns_router
from backend.app.api.investigations import router as investigations_router
from backend.app.api.evaluation import router as evaluation_router

logger = get_logger(__name__)


# ── Lifespan (startup / shutdown) ────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle: startup and shutdown hooks."""
    setup_logging(settings.LOG_LEVEL)
    logger.info(
        "ScamTrap AI starting",
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        llm_provider=settings.LLM_PROVIDER,
    )
    yield
    logger.info("ScamTrap AI shutting down")


# ── Request ID Middleware ────────────────────────────────────────────────

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Attaches a unique request ID to every request for tracing."""

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


# ── Application Factory ─────────────────────────────────────────────────

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    This is the single entry point for the backend. All middleware, routers,
    and error handlers are registered here.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "ScamTrap AI — Behavioral intelligence platform for scam campaign "
            "detection and investigation. Converts suspicious multilingual "
            "conversations into structured Scam DNA, correlates incidents, "
            "and discovers emerging campaigns."
        ),
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # ── CORS ─────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Request ID ───────────────────────────────────────────────────
    app.add_middleware(RequestIDMiddleware)

    # ── Global Exception Handlers ────────────────────────────────────

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        request_id = getattr(request.state, "request_id", "unknown")
        logger.warning(
            "Validation error",
            request_id=request_id,
            error=str(exc),
            path=str(request.url),
        )
        return JSONResponse(
            status_code=422,
            content={
                "error": "validation_error",
                "detail": str(exc),
                "request_id": request_id,
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        request_id = getattr(request.state, "request_id", "unknown")
        logger.error(
            "Unhandled exception",
            request_id=request_id,
            error=str(exc),
            error_type=type(exc).__name__,
            path=str(request.url),
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_server_error",
                "detail": "An unexpected error occurred."
                if not settings.DEBUG
                else str(exc),
                "request_id": request_id,
            },
        )

    # ── Routers ──────────────────────────────────────────────────────
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(auth_router)
    app.include_router(incidents_router)
    app.include_router(campaigns_router)
    app.include_router(investigations_router)
    app.include_router(evaluation_router)

    # Also mount health at root for simple Docker/LB probes
    app.include_router(health_router)

    return app


# The application instance — used by uvicorn
app = create_app()
