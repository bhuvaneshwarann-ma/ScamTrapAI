"""
ScamTrap AI — Database Engine & Session Management

Supports PostgreSQL (production) and SQLite (local dev/testing) without
changing domain logic. Uses SQLAlchemy 2.0 with the modern mapped_column API.

Usage:
    from backend.app.db.engine import get_db, init_db

    # In FastAPI dependency:
    async def endpoint(db: Session = Depends(get_db)):
        ...

    # At startup:
    init_db()  # Creates all tables
"""

import os
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

from backend.app.core.config import settings
from backend.app.core.logging import get_logger

logger = get_logger(__name__)


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all ORM models."""
    pass


def _create_engine():
    """Create the SQLAlchemy engine based on configuration."""
    url = settings.DATABASE_URL
    if os.getenv("VERCEL") and url.startswith("sqlite"):
        url = "sqlite:////tmp/scamtrap.db"

    # SQLite-specific configuration
    if url.startswith("sqlite"):
        engine = create_engine(
            url,
            connect_args={"check_same_thread": False},
            echo=settings.DEBUG,
            pool_pre_ping=True,
        )
        # Enable WAL mode and foreign keys for SQLite
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        return engine

    # PostgreSQL configuration
    return create_engine(
        url,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )


engine = _create_engine()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a database session.
    Automatically closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Create all tables defined in the ORM models.
    Call this at application startup.
    """
    # Import models to ensure they're registered with Base
    import backend.app.db.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized", url=settings.DATABASE_URL.split("@")[-1] if "@" in settings.DATABASE_URL else settings.DATABASE_URL)


def drop_db() -> None:
    """Drop all tables. Used in testing only."""
    Base.metadata.drop_all(bind=engine)
