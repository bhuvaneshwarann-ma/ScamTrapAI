"""
ScamTrap AI — Incident Schema

An Incident is the raw unit of input: a suspicious conversation (SMS, WhatsApp,
Email, Voice Transcript) submitted for analysis. After processing, it gains a
ScamDNA fingerprint, extracted entities, and relationships to other incidents.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List

from pydantic import BaseModel, Field

from backend.app.models.enums import IncidentChannel, IncidentStatus
from backend.app.models.scam_dna import ScamDNA


class IncidentCreate(BaseModel):
    """Schema for creating a new incident (ingest API)."""
    raw_text: str = Field(
        ...,
        min_length=1,
        max_length=50000,
        description="Raw text of the scam conversation/transcript."
    )
    channel: IncidentChannel = Field(
        default=IncidentChannel.OTHER,
        description="Communication channel."
    )
    reported_by: Optional[str] = Field(
        default=None,
        description="Anonymized reporter identifier."
    )
    metadata: Optional[dict] = Field(
        default=None,
        description="Additional metadata (e.g. device info, location region)."
    )


class Incident(BaseModel):
    """Full incident record with processing results."""
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique incident identifier."
    )
    raw_text: str = Field(
        ...,
        description="Raw text of the scam conversation/transcript."
    )
    channel: IncidentChannel = Field(
        default=IncidentChannel.SMS,
        description="Communication channel."
    )
    status: IncidentStatus = Field(
        default=IncidentStatus.PENDING,
        description="Processing status."
    )
    reported_by: Optional[str] = Field(
        default=None,
        description="Anonymized reporter identifier."
    )
    scam_dna: Optional[ScamDNA] = Field(
        default=None,
        description="Extracted Scam DNA (populated after Phase 4 analysis)."
    )
    entity_ids: List[str] = Field(
        default_factory=list,
        description="IDs of entities extracted from this incident."
    )
    relationship_ids: List[str] = Field(
        default_factory=list,
        description="IDs of relationships involving this incident."
    )
    campaign_id: Optional[str] = Field(
        default=None,
        description="Campaign this incident belongs to (if detected)."
    )
    # Ground truth — hidden from investigator UI, used for evaluation only
    ground_truth_campaign_id: Optional[str] = Field(
        default=None,
        description="Ground truth campaign ID for evaluation (synthetic data only). "
                    "NEVER shown in the investigator UI."
    )
    metadata: Optional[dict] = Field(
        default=None,
        description="Additional metadata."
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When the incident was ingested."
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When the incident was last updated."
    )


class IncidentSummary(BaseModel):
    """Lightweight incident summary for list views."""
    id: str
    channel: IncidentChannel
    status: IncidentStatus
    language: Optional[str] = None
    impersonation_target: Optional[str] = None
    campaign_id: Optional[str] = None
    created_at: datetime
