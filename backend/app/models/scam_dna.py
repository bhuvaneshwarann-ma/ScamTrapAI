"""
ScamTrap AI — Scam DNA Schema (§3.4)

The Scam DNA is the structured behavioral fingerprint extracted from a scam
incident. The LLM extractor (Phase 4) populates this schema by classifying
into the locked enums from §3.3 — it does NOT generate free text for enum fields.
"""

from typing import List, Optional

from pydantic import BaseModel, Field

from backend.app.models.enums import (
    ImpersonationTarget,
    PaymentMethod,
    SocialEngineeringTactic,
    IncidentChannel,
)


class ScamDNA(BaseModel):
    """
    Full Scam DNA Schema (§3.4).

    This is the structured behavioral fingerprint of a scam incident.
    All enum fields are classified into the locked taxonomy — deterministic
    set-intersection is possible without LLM involvement.
    """
    language: str = Field(
        ...,
        description="Detected language of the incident (e.g. 'en', 'ta', 'hi', 'ta-en')."
    )
    channel: IncidentChannel = Field(
        ...,
        description="Communication channel (SMS, WhatsApp, Email, Voice)."
    )
    impersonation_target: ImpersonationTarget = Field(
        ...,
        description="Who the scammer is impersonating."
    )
    impersonation_target_detail: Optional[str] = Field(
        default=None,
        description="Free-text detail when impersonation_target is 'other'."
    )
    urgency: float = Field(
        ge=0.0, le=1.0,
        description="Degree of urgency pressure detected (0.0–1.0)."
    )
    fear: float = Field(
        ge=0.0, le=1.0,
        description="Degree of fear induction detected (0.0–1.0)."
    )
    authority_pressure: float = Field(
        ge=0.0, le=1.0,
        description="Degree of authority pressure detected (0.0–1.0)."
    )
    credential_request: bool = Field(
        ...,
        description="Whether the scammer requested credentials (passwords, OTPs, PINs)."
    )
    payment_request: bool = Field(
        ...,
        description="Whether the scammer requested a payment."
    )
    payment_method: PaymentMethod = Field(
        ...,
        description="Payment method requested by the scammer."
    )
    requested_action: str = Field(
        ...,
        description="What the scammer asked the victim to do."
    )
    social_engineering_tactics: List[SocialEngineeringTactic] = Field(
        default_factory=list,
        description="Social engineering tactics used (from locked taxonomy)."
    )
    target_type: str = Field(
        ...,
        description="Type of victim targeted (e.g. 'individual', 'business', 'elderly')."
    )
    script_features: List[str] = Field(
        default_factory=list,
        description="Notable script features (e.g. 'greeting pattern', 'specific time reference')."
    )
    infrastructure_indicators: List[str] = Field(
        default_factory=list,
        description="Infrastructure indicators found (e.g. 'burner phone', 'VPN detected')."
    )
    # Extracted identifiers (raw — entity resolution happens in Phase 5)
    phone_numbers: List[str] = Field(
        default_factory=list,
        description="Phone numbers extracted from the incident."
    )
    upi_ids: List[str] = Field(
        default_factory=list,
        description="UPI IDs extracted from the incident."
    )
    urls: List[str] = Field(
        default_factory=list,
        description="URLs extracted from the incident."
    )
    domains: List[str] = Field(
        default_factory=list,
        description="Domains extracted from the incident."
    )
    emails: List[str] = Field(
        default_factory=list,
        description="Email addresses extracted from the incident."
    )
    extraction_confidence: float = Field(
        ge=0.0, le=1.0,
        description="How sure the Scam DNA extractor is about the fields it extracted. "
                    "Namespaced confidence (§3.2) — backend/diagnostics only."
    )
