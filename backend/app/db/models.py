"""
ScamTrap AI — SQLAlchemy ORM Models

All database tables are defined here. These map 1:1 to the Pydantic domain
models in backend/app/models/ but are the persistence layer. The Pydantic
schemas handle validation and serialization; these handle storage.

Indexes are defined per the spec:
  - incident timestamp, phone number, UPI, URL, domain
  - campaign ID, relationship, embedding reference
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    String,
    Text,
    Float,
    Boolean,
    DateTime,
    Integer,
    ForeignKey,
    Index,
    JSON,
)
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import Optional, List

from backend.app.db.engine import Base


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ═══════════════════════════════════════════════════════════════════════════
# Incident
# ═══════════════════════════════════════════════════════════════════════════

class IncidentDB(Base):
    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    channel: Mapped[str] = mapped_column(String(20), nullable=False, default="other")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    reported_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Scam DNA (stored as JSON — deserialized into Pydantic ScamDNA)
    scam_dna: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)

    # Campaign membership
    campaign_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("campaigns.id"), nullable=True
    )

    # Ground truth for evaluation (synthetic data only)
    ground_truth_campaign_id: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )

    # Metadata
    metadata_json: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_now, onupdate=_now, nullable=False)

    # Relationships
    entity_mentions: Mapped[List["EntityMentionDB"]] = relationship(
        back_populates="incident", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_incident_created_at", "created_at"),
        Index("idx_incident_campaign_id", "campaign_id"),
        Index("idx_incident_status", "status"),
        Index("idx_incident_channel", "channel"),
        Index("idx_incident_ground_truth", "ground_truth_campaign_id"),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Entity
# ═══════════════════════════════════════════════════════════════════════════

class EntityDB(Base):
    __tablename__ = "entities"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    entity_type: Mapped[str] = mapped_column(String(20), nullable=False)
    normalized_value: Mapped[str] = mapped_column(String(500), nullable=False)

    # Namespaced confidence (§3.2)
    resolution_confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    # Temporal
    first_seen: Mapped[datetime] = mapped_column(DateTime, default=_now, nullable=False)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=_now, nullable=False)

    # Metadata
    metadata_json: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)

    # Relationships
    mentions: Mapped[List["EntityMentionDB"]] = relationship(
        back_populates="entity", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_entity_type", "entity_type"),
        Index("idx_entity_normalized_value", "normalized_value"),
        Index("idx_entity_type_value", "entity_type", "normalized_value", unique=True),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Entity Mention (join between Incident and Entity)
# ═══════════════════════════════════════════════════════════════════════════

class EntityMentionDB(Base):
    __tablename__ = "entity_mentions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    incident_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("incidents.id"), nullable=False
    )
    entity_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("entities.id"), nullable=True
    )
    entity_type: Mapped[str] = mapped_column(String(20), nullable=False)
    raw_value: Mapped[str] = mapped_column(String(500), nullable=False)
    context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now, nullable=False)

    # Relationships
    incident: Mapped["IncidentDB"] = relationship(back_populates="entity_mentions")
    entity: Mapped[Optional["EntityDB"]] = relationship(back_populates="mentions")

    __table_args__ = (
        Index("idx_mention_incident_id", "incident_id"),
        Index("idx_mention_entity_id", "entity_id"),
        Index("idx_mention_entity_type", "entity_type"),
        Index("idx_mention_raw_value", "raw_value"),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Relationship
# ═══════════════════════════════════════════════════════════════════════════

class RelationshipDB(Base):
    __tablename__ = "relationships"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    source_incident_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("incidents.id"), nullable=False
    )
    target_incident_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("incidents.id"), nullable=False
    )
    relationship_type: Mapped[str] = mapped_column(String(30), nullable=False)

    # Namespaced confidence (§3.2)
    relationship_probability: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    relationship_confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Evidence (stored as JSON list)
    supporting_evidence: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    feature_contributions: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_now, onupdate=_now, nullable=False)

    __table_args__ = (
        Index("idx_rel_source", "source_incident_id"),
        Index("idx_rel_target", "target_incident_id"),
        Index("idx_rel_type", "relationship_type"),
        Index("idx_rel_confidence", "relationship_confidence"),
        Index("idx_rel_verified", "is_verified"),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Campaign
# ═══════════════════════════════════════════════════════════════════════════

class CampaignDB(Base):
    __tablename__ = "campaigns"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="emerging")

    # Namespaced confidence (§3.2)
    campaign_confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    risk_level: Mapped[str] = mapped_column(String(20), nullable=False, default="low")

    # Evidence & intelligence (JSON)
    supporting_evidence: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    shared_infrastructure: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    shared_tactics: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)

    # Temporal
    first_seen: Mapped[datetime] = mapped_column(DateTime, default=_now, nullable=False)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=_now, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_now, onupdate=_now, nullable=False)

    # Relationships
    incidents: Mapped[List["IncidentDB"]] = relationship()

    __table_args__ = (
        Index("idx_campaign_status", "status"),
        Index("idx_campaign_confidence", "campaign_confidence"),
        Index("idx_campaign_risk", "risk_level"),
        Index("idx_campaign_first_seen", "first_seen"),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Evidence (persistent storage for evidence records)
# ═══════════════════════════════════════════════════════════════════════════

class EvidenceDB(Base):
    __tablename__ = "evidence"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    claim: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)  # OBSERVED/INFERRED/PREDICTED
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    evidence_confidence: Mapped[float] = mapped_column(Float, nullable=False)

    # References
    relationship_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("relationships.id"), nullable=True
    )
    campaign_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("campaigns.id"), nullable=True
    )

    # Supporting data (JSON)
    supporting_incident_ids: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    supporting_entity_ids: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    scoring_factors: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)

    # Timestamps
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=_now, nullable=False)

    __table_args__ = (
        Index("idx_evidence_type", "type"),
        Index("idx_evidence_source", "source"),
        Index("idx_evidence_relationship", "relationship_id"),
        Index("idx_evidence_campaign", "campaign_id"),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Embedding Reference (for Phase 6+)
# ═══════════════════════════════════════════════════════════════════════════

class EmbeddingDB(Base):
    __tablename__ = "embeddings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    incident_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("incidents.id"), nullable=False, unique=True
    )
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    # Embedding vector stored as JSON array (pgvector column in production)
    embedding_vector: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now, nullable=False)

    __table_args__ = (
        Index("idx_embedding_incident", "incident_id"),
        Index("idx_embedding_model", "model_name"),
    )
