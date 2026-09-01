"""
ScamTrap AI — Canonical Evidence Object (§3.1)

Defined ONCE here in Phase 2. No later phase redefines this schema.
Phases 7, 9, and 10 consume and populate it — they do not modify the schema.

The Evidence object is the atomic unit of provenance in ScamTrap AI. Every
claim, relationship, and campaign assessment is backed by one or more Evidence
records, each carrying:
  - A provenance type (OBSERVED / INFERRED / PREDICTED)
  - A source subsystem identifier
  - A namespaced confidence score
  - Supporting references (incident IDs, entity IDs)
  - Scoring factor breakdown
"""

from datetime import datetime, timezone
from typing import List, Dict

from pydantic import BaseModel, Field, ConfigDict

from backend.app.models.enums import ProvenanceType


class Evidence(BaseModel):
    """
    Canonical Evidence Object (§3.1).

    This is immutable after creation — it represents a point-in-time claim
    with its provenance chain. To update an assessment, create a new Evidence
    record rather than mutating an existing one.
    """
    model_config = ConfigDict(frozen=True)

    claim: str = Field(
        ...,
        description="Human-readable description of the evidential claim."
    )
    type: ProvenanceType = Field(
        ...,
        description="Provenance: OBSERVED (ground truth), INFERRED (heuristic/NLP), "
                    "or PREDICTED (ML model output)."
    )
    source: str = Field(
        ...,
        description="Subsystem that produced this claim, e.g. 'entity_resolver', "
                    "'dna_extractor', 'similarity_service', 'relationship_engine'."
    )
    # Namespaced confidence — this field is intentionally generic in the Evidence
    # object; the consumer (relationship, campaign) applies the correct namespace.
    evidence_confidence: float = Field(
        ge=0.0, le=1.0,
        description="Confidence score for this specific piece of evidence. "
                    "Consumers map this to their namespaced confidence field."
    )
    supporting_incident_ids: List[str] = Field(
        default_factory=list,
        description="Incident IDs that support this claim."
    )
    supporting_entity_ids: List[str] = Field(
        default_factory=list,
        description="Entity IDs that support this claim."
    )
    scoring_factors: Dict[str, float] = Field(
        default_factory=dict,
        description="Breakdown of factors that contributed to the confidence score. "
                    "E.g. {'shared_upi': 0.9, 'temporal_proximity': 0.3}."
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When this evidence was generated."
    )
