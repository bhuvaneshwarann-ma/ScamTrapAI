"""
ScamTrap AI — Entity & Entity Mention Schemas

Entities are normalized, canonical identifiers extracted from incidents.
An Entity represents a unique real-world identifier (phone number, UPI ID,
email, URL, domain). EntityMention represents each raw occurrence of that
identifier in an incident, before normalization.

Entity Resolution (Phase 5) converts multiple EntityMentions into a single
canonical Entity with a resolution_confidence score.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field

from backend.app.models.enums import EntityType


class EntityMention(BaseModel):
    """
    A raw mention of an identifier in an incident, before normalization.
    Multiple mentions may resolve to the same canonical Entity.
    """
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique mention identifier."
    )
    incident_id: str = Field(
        ...,
        description="The incident this mention was extracted from."
    )
    entity_type: EntityType = Field(
        ...,
        description="Type of entity (PHONE, UPI, EMAIL, URL, DOMAIN)."
    )
    raw_value: str = Field(
        ...,
        description="The raw value as it appeared in the incident text."
    )
    canonical_entity_id: Optional[str] = Field(
        default=None,
        description="The canonical Entity this mention resolved to (set by entity resolver)."
    )
    context: Optional[str] = Field(
        default=None,
        description="Surrounding text context where the mention was found."
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class Entity(BaseModel):
    """
    A canonical, normalized entity — the result of entity resolution.
    Multiple EntityMentions from different incidents may resolve to the
    same Entity, which is a key signal for campaign detection.
    """
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique canonical entity identifier."
    )
    entity_type: EntityType = Field(
        ...,
        description="Type of entity."
    )
    normalized_value: str = Field(
        ...,
        description="Normalized, canonical value (e.g. E.164 phone, lowercase UPI)."
    )
    mention_ids: List[str] = Field(
        default_factory=list,
        description="IDs of all EntityMentions that resolved to this Entity."
    )
    incident_ids: List[str] = Field(
        default_factory=list,
        description="IDs of all incidents that reference this entity."
    )
    resolution_confidence: float = Field(
        ge=0.0, le=1.0,
        default=1.0,
        description="How sure the entity resolver is that all mentions are the same entity. "
                    "Namespaced confidence (§3.2)."
    )
    first_seen: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When this entity was first observed."
    )
    last_seen: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When this entity was most recently observed."
    )
    metadata: Optional[dict] = Field(
        default=None,
        description="Additional metadata."
    )
