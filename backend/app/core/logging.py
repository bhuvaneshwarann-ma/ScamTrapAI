"""
ScamTrap AI — Structured JSON Logger with Automatic PII Redaction

Cross-cutting constraint (§4.2): no raw PII (phone numbers, emails, UPI IDs,
URLs) may appear in any log output. This module configures ``structlog`` to
automatically detect and replace PII patterns with HMAC-hashed tokens before
the log line is emitted.

Usage:
    from backend.app.core.logging import get_logger
    logger = get_logger(__name__)
    logger.info("Processing incident", phone="+91 98765 43210")
    # Output: {"phone": "PH:a3f8c2d1e5...", ...}
"""

import re
import logging
import sys
from typing import Any

import structlog

from backend.app.core.security import hash_pii


# ── PII detection regex patterns ────────────────────────────────────────
# These patterns match common PII formats in log values and messages.

_PII_PATTERNS = [
    # Phone numbers: +91 98765 43210, 9876543210, +1-555-123-4567, etc.
    (
        re.compile(
            r"(\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{3,5}[-.\s]?\d{3,5})"
        ),
        "phone",
    ),
    # UPI IDs: user@bankname — checked BEFORE general email pattern
    # because UPI IDs (e.g. fraud@ybl) look like emails but are more specific
    (
        re.compile(
            r"([a-zA-Z0-9._\-]+@(?:ybl|paytm|okicici|okhdfcbank|oksbi|okaxis|apl|ibl|upi|axl|sbi|hdfcbank|icici|kotak|pnb|boi|cbi|unionbank|cnrb|utbi|dbs|indus|kvb|Federal|rbl|idbi|allbank|aubank|equitas|bandhan|yes|dlb|karur|lvb|tjsb|uco|idfc|nsdl|airtel|freecharge|jio|slice|amazonpay|gpay|phonepe|whatsapp))"
        ),
        "upi",
    ),
    # Email addresses (general — after UPI to avoid false matches)
    (
        re.compile(
            r"([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})"
        ),
        "email",
    ),
    # URLs: http(s)://...
    (
        re.compile(
            r"(https?://[^\s<>\"']+)"
        ),
        "url",
    ),
]


def _redact_pii_in_value(value: Any) -> Any:
    """Recursively redact PII in a log value (string, dict, or list)."""
    if isinstance(value, str):
        result = value
        # UPI check first (more specific) then general patterns
        for pattern, pii_type in _PII_PATTERNS:
            result = pattern.sub(
                lambda m, pt=pii_type: hash_pii(m.group(1), pt),
                result,
            )
        return result
    elif isinstance(value, dict):
        return {k: _redact_pii_in_value(v) for k, v in value.items()}
    elif isinstance(value, (list, tuple)):
        return type(value)(_redact_pii_in_value(item) for item in value)
    return value


def _pii_redaction_processor(
    logger: Any, method_name: str, event_dict: dict
) -> dict:
    """
    Structlog processor that scans every value in the event dict for PII
    patterns and replaces them with HMAC-hashed tokens.
    """
    for key, value in list(event_dict.items()):
        event_dict[key] = _redact_pii_in_value(value)
    return event_dict


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure structlog for JSON output with automatic PII redaction.

    Call once at application startup (in main.py). All subsequent calls to
    ``get_logger()`` will inherit this configuration.
    """
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.UnicodeDecoder(),
            _pii_redaction_processor,  # ← PII redaction happens here
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure the root stdlib logger to output at the desired level
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Clear existing handlers and add a single stream handler
    root_logger.handlers.clear()
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    root_logger.addHandler(handler)


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Get a named, structured logger with PII redaction enabled.

    Args:
        name: Logger name (typically ``__name__``).

    Returns:
        A bound structlog logger.
    """
    return structlog.get_logger(name)
