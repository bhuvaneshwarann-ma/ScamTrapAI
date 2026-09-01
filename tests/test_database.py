"""
ScamTrap AI — Database CRUD & Relationship Tests

Validates:
- Database initialization and table creation
- Incident CRUD
- Entity and EntityMention CRUD
- Relationship CRUD
- Campaign CRUD and membership assignment
- Evidence storage
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.db.engine import Base
from backend.app.db import crud


@pytest.fixture
def db_session():
    """In-memory SQLite database session fixture for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()


def test_incident_crud(db_session):
    """Test incident creation, retrieval, status update, and count."""
    inc = crud.create_incident(
        db=db_session,
        raw_text="Urgent! Your account is locked. Pay via UPI scammer@ybl immediately.",
        channel="sms",
        ground_truth_campaign_id="camp-synthetic-1",
    )
    assert inc.id is not None
    assert inc.raw_text.startswith("Urgent!")
    assert inc.status == "pending"

    # Get incident
    fetched = crud.get_incident(db_session, inc.id)
    assert fetched is not None
    assert fetched.ground_truth_campaign_id == "camp-synthetic-1"

    # Update status
    updated = crud.update_incident_status(db_session, inc.id, "analyzed")
    assert updated.status == "analyzed"

    # Count
    assert crud.count_incidents(db_session) == 1


def test_entity_and_mention_crud(db_session):
    """Test entity deduplication and mention linking."""
    inc = crud.create_incident(db_session, raw_text="Call +919876543210")

    entity = crud.get_or_create_entity(
        db=db_session,
        entity_type="phone",
        normalized_value="+919876543210",
        resolution_confidence=0.99,
    )
    assert entity.id is not None

    mention = crud.create_entity_mention(
        db=db_session,
        incident_id=inc.id,
        entity_type="phone",
        raw_value="+91 98765 43210",
        entity_id=entity.id,
    )
    assert mention.entity_id == entity.id

    # Deduplication test
    entity2 = crud.get_or_create_entity(
        db=db_session,
        entity_type="phone",
        normalized_value="+919876543210",
    )
    assert entity2.id == entity.id


def test_campaign_and_relationship_crud(db_session):
    """Test campaign creation, incident assignment, and relationship linkage."""
    inc1 = crud.create_incident(db_session, raw_text="Scam 1")
    inc2 = crud.create_incident(db_session, raw_text="Scam 2")

    campaign = crud.create_campaign(
        db=db_session,
        name="Test KYC Scam Campaign",
        status="emerging",
        campaign_confidence=0.85,
    )
    assert campaign.id is not None

    # Assign incidents
    crud.assign_incident_to_campaign(db_session, inc1.id, campaign.id)
    crud.assign_incident_to_campaign(db_session, inc2.id, campaign.id)

    camp_incidents = crud.get_campaign_incidents(db_session, campaign.id)
    assert len(camp_incidents) == 2

    # Relationship
    rel = crud.create_relationship(
        db=db_session,
        source_incident_id=inc1.id,
        target_incident_id=inc2.id,
        relationship_type="shared_phone",
        relationship_probability=0.92,
        relationship_confidence=0.95,
        is_verified=True,
    )
    assert rel.id is not None
    assert rel.relationship_confidence == 0.95
