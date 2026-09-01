"""
ScamTrap AI — PII Security Utilities

HMAC-SHA256 based deterministic hashing for PII (phones, emails, UPI IDs, URLs).
This is a cross-cutting constraint (§4.2): no raw identifier may ever appear in logs,
debug output, or non-essential storage. All identifiers pass through these helpers.

The hashing is deterministic so that the same raw value always resolves to the same
token — enabling correlation and deduplication without exposing the raw data in logs.
"""

import hashlib
import hmac
from typing import Literal

from backend.app.core.config import settings


PIIType = Literal["phone", "email", "upi", "url", "domain", "generic"]

# ── Prefix tags make hashed values self-describing in logs ───────────────
_PREFIX_MAP: dict[PIIType, str] = {
    "phone": "PH",
    "email": "EM",
    "upi": "UP",
    "url": "UR",
    "domain": "DM",
    "generic": "GN",
}


def hash_pii(value: str, pii_type: PIIType = "generic") -> str:
    """
    Deterministic HMAC-SHA256 hash of a PII value.

    Returns a prefixed, truncated hex digest that is safe to log and
    still useful for correlation (e.g. ``PH:a3f8c2d1``).

    Args:
        value: The raw PII string to hash.
        pii_type: The category of PII for prefix tagging.

    Returns:
        A string like ``PH:a3f8c2d1e5...`` (prefix + first 16 hex chars).
    """
    if not value:
        return f"{_PREFIX_MAP[pii_type]}:EMPTY"

    digest = hmac.new(
        key=settings.PII_HMAC_KEY.encode("utf-8"),
        msg=value.strip().encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()

    prefix = _PREFIX_MAP.get(pii_type, "GN")
    # 16 hex chars = 64 bits of hash — sufficient for log correlation,
    # astronomically unlikely to collide within a single investigation.
    return f"{prefix}:{digest[:16]}"


def hash_phone(phone: str) -> str:
    """Hash a phone number for safe logging."""
    return hash_pii(phone, "phone")


def hash_email(email: str) -> str:
    """Hash an email address for safe logging."""
    return hash_pii(email, "email")


def hash_upi(upi: str) -> str:
    """Hash a UPI ID for safe logging."""
    return hash_pii(upi, "upi")


def hash_url(url: str) -> str:
    """Hash a URL for safe logging."""
    return hash_pii(url, "url")


def hash_domain(domain: str) -> str:
    """Hash a domain name for safe logging."""
    return hash_pii(domain, "domain")
