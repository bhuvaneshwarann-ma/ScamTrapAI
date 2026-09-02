"""
ScamTrap AI — Investigation & Risk Assessment Schemas

RiskAssessment provides an overall risk score for an incident.
Investigation wraps a copilot interaction session with evidence-bounded Q&A.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field

from backend.app.models.enums import RiskLevel, ProvenanceType
from backend.app.models.evidence import Evidence


class RiskAssessment(BaseModel):
    """
    Risk assessment for an incident or campaign.
    All claims carry provenance — no bare assertions.
    """
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4())
    )
    target_id: str = Field(
        ...,
        description="ID of the incident or campaign being assessed."
    )
    target_type: str = Field(
        ...,
        description="'incident' or 'campaign'."
    )
    risk_level: RiskLevel = Field(
        ...,
        description="Overall risk level."
    )
    risk_score: float = Field(
        ge=0.0, le=1.0,
        description="Numerical risk score (0.0–1.0)."
    )
    provenance: ProvenanceType = Field(
        ...,
        description="How this assessment was derived."
    )
    factors: List[Evidence] = Field(
        default_factory=list,
        description="Evidence records that contribute to this assessment."
    )
    summary: str = Field(
        ...,
        description="Human-readable risk summary."
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class InvestigationQuery(BaseModel):
    """A query to the Evidence-Bounded Investigator Copilot."""
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The investigator's question."
    )
    context_incident_ids: List[str] = Field(
        default_factory=list,
        description="Incident IDs to scope the investigation to."
    )
    context_campaign_ids: List[str] = Field(
        default_factory=list,
        description="Campaign IDs to scope the investigation to."
    )


class InvestigationResponse(BaseModel):
    """Response from the Evidence-Bounded Investigator Copilot (§ Phase 8)."""
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4())
    )
    question: str = Field(
        ...,
        description="The original question."
    )
    assessment: Optional[str] = Field(
        default=None,
        description="Structured assessment summary (e.g. 'Likely associated with Campaign SC-1024')."
    )
    confidence: float = Field(
        default=0.0,
        ge=0.0, le=1.0,
        description="Grounding confidence score (0.0–1.0)."
    )
    answer: str = Field(
        ...,
        description="The copilot's evidence-bounded answer."
    )
    cited_evidence: List[Evidence] = Field(
        default_factory=list,
        description="Evidence records cited in the answer."
    )
    cited_incident_ids: List[str] = Field(
        default_factory=list,
        description="Incident IDs referenced in the answer."
    )
    cited_entity_ids: List[str] = Field(
        default_factory=list,
        description="Entity IDs referenced in the answer."
    )
    cited_relationship_ids: List[str] = Field(
        default_factory=list,
        description="Relationship IDs referenced in the answer."
    )
    insufficient_evidence: bool = Field(
        default=False,
        description="True if the copilot could not answer due to insufficient evidence."
    )
    model_name: str = Field(
        default="copilot-evidence-bounded-v1",
        description="Model identifier used for Q&A synthesis."
    )
    scam_dna_schema_version: str = Field(
        default="1.0",
        description="Scam DNA schema version used."
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
