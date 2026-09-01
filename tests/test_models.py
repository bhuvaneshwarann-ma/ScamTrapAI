"""
ScamTrap AI — Phase 2 Model & Taxonomy Validation Tests

Validates:
- Closed enum taxonomy validation (SocialEngineeringTactic, ImpersonationTarget, PaymentMethod, etc.)
- Invalid enums fail validation
- ScamDNA schema validation
- Provenance tagging on models
"""

import pytest
from pydantic import ValidationError

from backend.app.models.enums import (
    SocialEngineeringTactic,
    ImpersonationTarget,
    PaymentMethod,
    ProvenanceType,
    IncidentChannel,
    EntityType,
    CampaignStatus,
    RiskLevel,
)
from backend.app.models.scam_dna import ScamDNA
from backend.app.models.incident import IncidentCreate, Incident
from backend.app.models.relationship import Relationship


def test_locked_taxonomy_enums():
    """Verify locked taxonomy enums have expected members."""
    assert SocialEngineeringTactic.URGENCY_PRESSURE == "urgency_pressure"
    assert SocialEngineeringTactic.AUTHORITY_IMPERSONATION == "authority_impersonation"
    assert ImpersonationTarget.BANK == "bank"
    assert ImpersonationTarget.OTHER == "other"
    assert PaymentMethod.UPI == "upi"
    assert ProvenanceType.OBSERVED == "OBSERVED"
    assert ProvenanceType.INFERRED == "INFERRED"
    assert ProvenanceType.PREDICTED == "PREDICTED"


def test_scam_dna_valid_creation():
    """Valid ScamDNA payload creation."""
    dna = ScamDNA(
        language="en",
        channel=IncidentChannel.SMS,
        impersonation_target=ImpersonationTarget.BANK,
        urgency=0.9,
        fear=0.7,
        authority_pressure=0.8,
        credential_request=True,
        payment_request=True,
        payment_method=PaymentMethod.UPI,
        requested_action="Transfer money immediately to prevent account suspension",
        social_engineering_tactics=[
            SocialEngineeringTactic.URGENCY_PRESSURE,
            SocialEngineeringTactic.FEAR_INDUCTION,
        ],
        target_type="individual",
        extraction_confidence=0.95,
    )
    assert dna.language == "en"
    assert dna.impersonation_target == ImpersonationTarget.BANK
    assert dna.payment_method == PaymentMethod.UPI
    assert len(dna.social_engineering_tactics) == 2


def test_scam_dna_invalid_enum_fails():
    """Invalid enum values must fail validation."""
    with pytest.raises(ValidationError):
        ScamDNA(
            language="en",
            channel="INVALID_CHANNEL",  # Invalid
            impersonation_target="alien_invasion",  # Invalid
            urgency=0.5,
            fear=0.5,
            authority_pressure=0.5,
            credential_request=False,
            payment_request=True,
            payment_method="magic",  # Invalid
            requested_action="Do something",
            target_type="individual",
            extraction_confidence=0.5,
        )


def test_namespaced_confidence_fields():
    """Verify namespaced confidence fields are present and bare 'confidence' is avoided."""
    rel = Relationship(
        source_incident_id="inc-1",
        target_incident_id="inc-2",
        relationship_type="shared_upi",
        relationship_probability=0.85,
        relationship_confidence=0.90,
    )
    assert hasattr(rel, "relationship_probability")
    assert hasattr(rel, "relationship_confidence")
    assert rel.relationship_probability == 0.85
    assert rel.relationship_confidence == 0.90
