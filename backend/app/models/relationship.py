"""
ScamTrap AI — Relationship Schema

A Relationship represents a detected connection between two incidents.
It carries both:
  - relationship_probability: Raw ML-predicted likelihood (internal only)
  - relationship_confidence: Confidence after deterministic evidence verification
    (investigator-facing)

Hard rule (§3.2): relationship_probability alone can NEVER populate an
investigator-visible field. Only relationship_confidence (which requires
independent, deterministic evidence) can.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict

from pydantic import BaseModel, Field

from backend.app.models.enums import RelationshipType
from backend.app.models.evidence import Evidence


class Relationship(BaseModel):
    """
    A relationship between two incidents, with dual confidence scores
    and supporting evidence chain.
    """
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique relationship identifier."
    )
    source_incident_id: str = Field(
        ...,
        description="First incident in the relationship."
    )
    target_incident_id: str = Field(
        ...,
        description="Second incident in the relationship."
    )
    relationship_type: RelationshipType = Field(
        ...,
        description="Type of relationship detected."
    )

    # ── Namespaced Confidence (§3.2) ──────────────────────────────────
    relationship_probability: float = Field(
        ge=0.0, le=1.0,
        default=0.0,
        description="Raw ML-predicted likelihood, pre-verification. "
                    "INTERNAL ML ONLY — never shown to an investigator on its own."
    )
    relationship_confidence: float = Field(
        ge=0.0, le=1.0,
        default=0.0,
        description="Confidence AFTER deterministic evidence verification. "
                    "This is the only relationship score shown to investigators."
    )

    # ── Evidence Chain ────────────────────────────────────────────────
    supporting_evidence: List[Evidence] = Field(
        default_factory=list,
        description="Evidence records supporting this relationship."
    )
    feature_contributions: Dict[str, float] = Field(
        default_factory=dict,
        description="Feature contribution breakdown (e.g. {'shared_upi': 0.4, 'temporal': 0.2})."
    )
    explanation: Optional[str] = Field(
        default=None,
        description="Human-readable explanation of why this relationship exists."
    )
    is_verified: bool = Field(
        default=False,
        description="Whether this relationship has been deterministically verified."
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
