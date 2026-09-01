"""
ScamTrap AI — CRUD Operations

Database access layer for all domain entities. Uses SQLAlchemy 2.0 sessions
and maps between ORM models (db/models.py) and Pydantic schemas (models/).
"""

import json
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import select, func

from backend.app.db.models import (
    IncidentDB,
    EntityDB,
    EntityMentionDB,
    RelationshipDB,
    CampaignDB,
    EvidenceDB,
)
from backend.app.core.logging import get_logger

logger = get_logger(__name__)


# ═══════════════════════════════════════════════════════════════════════════
# Incident CRUD
# ═══════════════════════════════════════════════════════════════════════════

def create_incident(
    db: Session,
    raw_text: str,
    channel: str = "other",
    reported_by: Optional[str] = None,
    metadata: Optional[dict] = None,
    ground_truth_campaign_id: Optional[str] = None,
) -> IncidentDB:
    """Create a new incident."""
    incident = IncidentDB(
        raw_text=raw_text,
        channel=channel,
        reported_by=reported_by,
        metadata_json=metadata,
        ground_truth_campaign_id=ground_truth_campaign_id,
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    logger.info("Incident created", incident_id=incident.id, channel=channel)
    return incident


def get_incident(db: Session, incident_id: str) -> Optional[IncidentDB]:
    """Get a single incident by ID."""
    return db.get(IncidentDB, incident_id)


def list_incidents(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    channel: Optional[str] = None,
    campaign_id: Optional[str] = None,
) -> List[IncidentDB]:
    """List incidents with optional filtering."""
    query = select(IncidentDB).order_by(IncidentDB.created_at.desc())
    if status:
        query = query.where(IncidentDB.status == status)
    if channel:
        query = query.where(IncidentDB.channel == channel)
    if campaign_id:
        query = query.where(IncidentDB.campaign_id == campaign_id)
    query = query.offset(skip).limit(limit)
    return list(db.execute(query).scalars().all())


def update_incident_status(db: Session, incident_id: str, status: str) -> Optional[IncidentDB]:
    """Update incident processing status."""
    incident = db.get(IncidentDB, incident_id)
    if incident:
        incident.status = status
        incident.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(incident)
    return incident


def update_incident_scam_dna(db: Session, incident_id: str, scam_dna: dict) -> Optional[IncidentDB]:
    """Store extracted Scam DNA on an incident."""
    incident = db.get(IncidentDB, incident_id)
    if incident:
        incident.scam_dna = scam_dna
        incident.status = "analyzed"
        incident.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(incident)
    return incident


def assign_incident_to_campaign(
    db: Session, incident_id: str, campaign_id: str
) -> Optional[IncidentDB]:
    """Assign an incident to a campaign."""
    incident = db.get(IncidentDB, incident_id)
    if incident:
        incident.campaign_id = campaign_id
        incident.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(incident)
    return incident


def count_incidents(db: Session) -> int:
    """Count total incidents."""
    return db.execute(select(func.count(IncidentDB.id))).scalar_one()


# ═══════════════════════════════════════════════════════════════════════════
# Entity CRUD
# ═══════════════════════════════════════════════════════════════════════════

def create_entity(
    db: Session,
    entity_type: str,
    normalized_value: str,
    resolution_confidence: float = 1.0,
) -> EntityDB:
    """Create a new canonical entity."""
    entity = EntityDB(
        entity_type=entity_type,
        normalized_value=normalized_value,
        resolution_confidence=resolution_confidence,
    )
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def get_entity(db: Session, entity_id: str) -> Optional[EntityDB]:
    """Get a single entity by ID."""
    return db.get(EntityDB, entity_id)


def find_entity_by_value(
    db: Session, entity_type: str, normalized_value: str
) -> Optional[EntityDB]:
    """Find an entity by its normalized value."""
    query = select(EntityDB).where(
        EntityDB.entity_type == entity_type,
        EntityDB.normalized_value == normalized_value,
    )
    return db.execute(query).scalar_one_or_none()


def get_or_create_entity(
    db: Session,
    entity_type: str,
    normalized_value: str,
    resolution_confidence: float = 1.0,
) -> EntityDB:
    """Get an existing entity or create a new one."""
    entity = find_entity_by_value(db, entity_type, normalized_value)
    if entity:
        entity.last_seen = datetime.now(timezone.utc)
        db.commit()
        return entity
    return create_entity(db, entity_type, normalized_value, resolution_confidence)


def list_entities(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    entity_type: Optional[str] = None,
) -> List[EntityDB]:
    """List entities with optional type filtering."""
    query = select(EntityDB)
    if entity_type:
        query = query.where(EntityDB.entity_type == entity_type)
    query = query.offset(skip).limit(limit)
    return list(db.execute(query).scalars().all())


# ═══════════════════════════════════════════════════════════════════════════
# Entity Mention CRUD
# ═══════════════════════════════════════════════════════════════════════════

def create_entity_mention(
    db: Session,
    incident_id: str,
    entity_type: str,
    raw_value: str,
    entity_id: Optional[str] = None,
    context: Optional[str] = None,
) -> EntityMentionDB:
    """Create a new entity mention."""
    mention = EntityMentionDB(
        incident_id=incident_id,
        entity_type=entity_type,
        raw_value=raw_value,
        entity_id=entity_id,
        context=context,
    )
    db.add(mention)
    db.commit()
    db.refresh(mention)
    return mention


def get_mentions_for_incident(db: Session, incident_id: str) -> List[EntityMentionDB]:
    """Get all entity mentions for an incident."""
    query = select(EntityMentionDB).where(EntityMentionDB.incident_id == incident_id)
    return list(db.execute(query).scalars().all())


def get_mentions_for_entity(db: Session, entity_id: str) -> List[EntityMentionDB]:
    """Get all mentions that resolved to a given entity."""
    query = select(EntityMentionDB).where(EntityMentionDB.entity_id == entity_id)
    return list(db.execute(query).scalars().all())


# ═══════════════════════════════════════════════════════════════════════════
# Relationship CRUD
# ═══════════════════════════════════════════════════════════════════════════

def create_relationship(
    db: Session,
    source_incident_id: str,
    target_incident_id: str,
    relationship_type: str,
    relationship_probability: float = 0.0,
    relationship_confidence: float = 0.0,
    supporting_evidence: Optional[list] = None,
    feature_contributions: Optional[dict] = None,
    explanation: Optional[str] = None,
    is_verified: bool = False,
) -> RelationshipDB:
    """Create a new relationship between two incidents."""
    rel = RelationshipDB(
        source_incident_id=source_incident_id,
        target_incident_id=target_incident_id,
        relationship_type=relationship_type,
        relationship_probability=relationship_probability,
        relationship_confidence=relationship_confidence,
        supporting_evidence=supporting_evidence,
        feature_contributions=feature_contributions,
        explanation=explanation,
        is_verified=is_verified,
    )
    db.add(rel)
    db.commit()
    db.refresh(rel)
    return rel


def get_relationship(db: Session, relationship_id: str) -> Optional[RelationshipDB]:
    """Get a single relationship by ID."""
    return db.get(RelationshipDB, relationship_id)


def get_relationships_for_incident(db: Session, incident_id: str) -> List[RelationshipDB]:
    """Get all relationships involving an incident."""
    query = select(RelationshipDB).where(
        (RelationshipDB.source_incident_id == incident_id) |
        (RelationshipDB.target_incident_id == incident_id)
    )
    return list(db.execute(query).scalars().all())


def list_relationships(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    verified_only: bool = False,
) -> List[RelationshipDB]:
    """List relationships with optional filtering."""
    query = select(RelationshipDB).order_by(RelationshipDB.created_at.desc())
    if verified_only:
        query = query.where(RelationshipDB.is_verified == True)  # noqa: E712
    query = query.offset(skip).limit(limit)
    return list(db.execute(query).scalars().all())


# ═══════════════════════════════════════════════════════════════════════════
# Campaign CRUD
# ═══════════════════════════════════════════════════════════════════════════

def create_campaign(
    db: Session,
    name: Optional[str] = None,
    status: str = "emerging",
    campaign_confidence: float = 0.0,
    risk_level: str = "low",
) -> CampaignDB:
    """Create a new campaign."""
    campaign = CampaignDB(
        name=name,
        status=status,
        campaign_confidence=campaign_confidence,
        risk_level=risk_level,
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    logger.info("Campaign created", campaign_id=campaign.id, name=name)
    return campaign


def get_campaign(db: Session, campaign_id: str) -> Optional[CampaignDB]:
    """Get a single campaign by ID."""
    return db.get(CampaignDB, campaign_id)


def list_campaigns(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
) -> List[CampaignDB]:
    """List campaigns with optional status filtering."""
    query = select(CampaignDB).order_by(CampaignDB.created_at.desc())
    if status:
        query = query.where(CampaignDB.status == status)
    query = query.offset(skip).limit(limit)
    return list(db.execute(query).scalars().all())


def update_campaign_confidence(
    db: Session, campaign_id: str, campaign_confidence: float
) -> Optional[CampaignDB]:
    """Update campaign confidence score."""
    campaign = db.get(CampaignDB, campaign_id)
    if campaign:
        campaign.campaign_confidence = campaign_confidence
        campaign.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(campaign)
    return campaign


def get_campaign_incidents(db: Session, campaign_id: str) -> List[IncidentDB]:
    """Get all incidents belonging to a campaign."""
    query = select(IncidentDB).where(IncidentDB.campaign_id == campaign_id)
    return list(db.execute(query).scalars().all())


def count_campaigns(db: Session) -> int:
    """Count total campaigns."""
    return db.execute(select(func.count(CampaignDB.id))).scalar_one()


# ═══════════════════════════════════════════════════════════════════════════
# Evidence CRUD
# ═══════════════════════════════════════════════════════════════════════════

def create_evidence(
    db: Session,
    claim: str,
    evidence_type: str,
    source: str,
    evidence_confidence: float,
    relationship_id: Optional[str] = None,
    campaign_id: Optional[str] = None,
    supporting_incident_ids: Optional[list] = None,
    supporting_entity_ids: Optional[list] = None,
    scoring_factors: Optional[dict] = None,
) -> EvidenceDB:
    """Create a new evidence record."""
    evidence = EvidenceDB(
        claim=claim,
        type=evidence_type,
        source=source,
        evidence_confidence=evidence_confidence,
        relationship_id=relationship_id,
        campaign_id=campaign_id,
        supporting_incident_ids=supporting_incident_ids,
        supporting_entity_ids=supporting_entity_ids,
        scoring_factors=scoring_factors,
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    return evidence


def get_evidence_for_relationship(db: Session, relationship_id: str) -> List[EvidenceDB]:
    """Get all evidence for a relationship."""
    query = select(EvidenceDB).where(EvidenceDB.relationship_id == relationship_id)
    return list(db.execute(query).scalars().all())


def get_evidence_for_campaign(db: Session, campaign_id: str) -> List[EvidenceDB]:
    """Get all evidence for a campaign."""
    query = select(EvidenceDB).where(EvidenceDB.campaign_id == campaign_id)
    return list(db.execute(query).scalars().all())
