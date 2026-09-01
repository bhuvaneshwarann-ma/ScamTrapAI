"""
ScamTrap AI — Configuration System

Pydantic Settings for centralized, env-driven configuration.
All secrets and tunables are sourced from environment variables / .env file.
"""

from typing import List

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application-wide configuration. Every value can be overridden via env vars."""

    # ── Application ──────────────────────────────────────────────────────
    APP_NAME: str = "ScamTrap AI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # ── Networking / CORS ────────────────────────────────────────────────
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins for the frontend.",
    )

    # ── Security ─────────────────────────────────────────────────────────
    PII_HMAC_KEY: str = Field(
        default="CHANGE_ME_IN_PRODUCTION_USE_A_REAL_SECRET_KEY",
        description="HMAC-SHA256 key used for deterministic PII hashing. "
        "MUST be changed in production.",
    )

    # ── Database (Phase 2+) ──────────────────────────────────────────────
    DATABASE_URL: str = Field(
        default="sqlite:///./scamtrap.db",
        description="SQLAlchemy connection string. PostgreSQL recommended for prod.",
    )

    # ── Redis (Phase 2+) ─────────────────────────────────────────────────
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection string for caching and token revocation.",
    )

    # ── AI / LLM (Phase 4+) ─────────────────────────────────────────────
    LLM_PROVIDER: str = Field(
        default="mock",
        description="LLM provider to use: 'ollama', 'gemini', or 'mock'. "
        "Mock provides deterministic offline fallback.",
    )
    GEMINI_API_KEY: str = Field(
        default="",
        description="Google Gemini API key. Required only when LLM_PROVIDER='gemini'.",
    )
    OLLAMA_BASE_URL: str = Field(
        default="http://localhost:11434",
        description="Local Ollama base URL.",
    )
    OLLAMA_MODEL: str = Field(
        default="llama3",
        description="Local Ollama model name (e.g. 'llama3', 'mistral', 'gemma', 'phi3', 'tinyllama').",
    )

    # ── Embedding (Phase 6+) ─────────────────────────────────────────────
    EMBEDDING_PROVIDER: str = Field(
        default="mock",
        description="Embedding provider: 'sentence-transformers' or 'mock'.",
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


# Singleton instance — import this, not the class
settings = Settings()
