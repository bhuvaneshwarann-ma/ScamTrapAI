"""
ScamTrap AI — Campaign Schema

A Campaign is a group of related incidents that share infrastructure,
behavioral patterns, and/or temporal proximity — detected through the
hybrid ML + deterministic verification pipeline.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field

from backend.app.models.enums import CampaignStatus, RiskLevel
from backend.app.models.evidence import Evidence


class TimelineItem(BaseModel):
    """Timeline entry representing incident/indicator progression over time."""
    timestamp: datetime
    event_type: str  # e.g., 'INCIDENT_OBSERVED', 'NEW_INFRASTRUCTURE', 'NEW_TACTIC'
    channel: Optional[str] = None
    description: str
    incident_id: Optional[str] = None
    indicators: List[str] = Field(default_factory=list)


class Campaign(BaseModel):
    """
    A detected scam campaign — a cluster of related incidents.
    """
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique campaign identifier."
    )
    name: Optional[str] = Field(
        default=None,
        description="Auto-generated or investigator-assigned campaign name."
    )
    status: CampaignStatus = Field(
        default=CampaignStatus.EMERGING,
        description="Current campaign status."
    )

    # ── Campaign Members ──────────────────────────────────────────────
    incident_ids: List[str] = Field(
        default_factory=list,
        description="IDs of incidents belonging to this campaign."
    )
    entity_ids: List[str] = Field(
        default_factory=list,
        description="IDs of shared entities across campaign incidents."
    )
    relationship_ids: List[str] = Field(
        default_factory=list,
        description="IDs of relationships within this campaign."
    )

    # ── Namespaced Confidence (§3.2) ──────────────────────────────────
    campaign_confidence: float = Field(
        ge=0.0, le=1.0,
        default=0.0,
        description="Confidence in the campaign grouping as a whole, aggregated "
                    "from relationship_confidence values. Investigator-facing."
    )

    # ── Campaign Intelligence ─────────────────────────────────────────
    risk_level: RiskLevel = Field(
        default=RiskLevel.LOW,
        description="Overall risk assessment."
    )
    supporting_evidence: List[Evidence] = Field(
        default_factory=list,
        description="Evidence records supporting the campaign detection."
    )
    shared_infrastructure: List[str] = Field(
        default_factory=list,
        description="Shared infrastructure indicators (phones, UPIs, URLs, domains)."
    )
    shared_tactics: List[str] = Field(
        default_factory=list,
        description="Shared social engineering tactics across incidents."
    )
    timeline: List[TimelineItem] = Field(
        default_factory=list,
        description="Chronological timeline of attack evolution across incidents."
    )

    # ── Temporal ──────────────────────────────────────────────────────
    first_seen: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When the first incident in this campaign was observed."
    )
    last_seen: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When the most recent incident was observed."
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class CampaignSummary(BaseModel):
    """Lightweight campaign summary for list views and alerts."""
    id: str
    name: Optional[str] = None
    status: CampaignStatus
    incident_count: int = 0
    entity_count: int = 0
    campaign_confidence: float = 0.0
    risk_level: RiskLevel = RiskLevel.LOW
    first_seen: datetime
    last_seen: datetime


class CampaignAlert(BaseModel):
    """Alert payload when an emerging campaign is detected."""
    campaign_id: str
    alert_type: str = "EMERGING_CAMPAIGN_DETECTED"
    incident_count: int
    entity_count: int
    campaign_confidence: float
    risk_level: RiskLevel
    shared_infrastructure: List[str]
    shared_tactics: List[str]
    supporting_evidence: List[Evidence]
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
