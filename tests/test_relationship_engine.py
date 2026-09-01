"""
ScamTrap AI — Phase 7 Relationship Engine Tests

Validates:
- High ML probability alone CANNOT produce high relationship_confidence
- Deterministic infrastructure match produces high relationship_confidence + Evidence
- Unverified candidates are marked is_verified=False
"""

import pytest
from datetime import datetime, timezone
from backend.app.models.enums import IncidentChannel, ImpersonationTarget, PaymentMethod, SocialEngineeringTactic
from backend.app.models.incident import Incident
from backend.app.models.scam_dna import ScamDNA
from backend.app.services.relationship_engine import RelationshipEngine


def test_ml_alone_cannot_produce_high_confidence():
    """Verify that high ML probability without deterministic evidence stays low confidence."""
    engine = RelationshipEngine()

    dna1 = ScamDNA(
        language="en", channel=IncidentChannel.SMS, impersonation_target=ImpersonationTarget.BANK,
        urgency=0.9, fear=0.8, authority_pressure=0.8, credential_request=True, payment_request=True,
        payment_method=PaymentMethod.UPI, requested_action="Update KYC",
        social_engineering_tactics=[SocialEngineeringTactic.URGENCY_PRESSURE], target_type="individual",
        extraction_confidence=0.95, phone_numbers=["+919000000001"], upi_ids=["user1@ybl"]
    )

    dna2 = ScamDNA(
        language="en", channel=IncidentChannel.SMS, impersonation_target=ImpersonationTarget.BANK,
        urgency=0.9, fear=0.8, authority_pressure=0.8, credential_request=True, payment_request=True,
        payment_method=PaymentMethod.UPI, requested_action="Update KYC",
        social_engineering_tactics=[SocialEngineeringTactic.URGENCY_PRESSURE], target_type="individual",
        extraction_confidence=0.95, phone_numbers=["+919000000002"], upi_ids=["user2@ybl"]
    )

    inc1 = Incident(raw_text="Inc 1", channel=IncidentChannel.SMS, scam_dna=dna1)
    inc2 = Incident(raw_text="Inc 2", channel=IncidentChannel.SMS, scam_dna=dna2)

    rel = engine.evaluate_pair(inc1, inc2)
    assert rel is not None
    assert rel.relationship_probability > 0.40
    # HARD RULE: Without deterministic shared infrastructure, confidence must be <= 0.40 and unverified
    assert rel.relationship_confidence <= 0.40
    assert not rel.is_verified


def test_deterministic_infrastructure_verification():
    """Verify shared UPI produces high confidence and verified relationship."""
    engine = RelationshipEngine()

    dna1 = ScamDNA(
        language="en", channel=IncidentChannel.SMS, impersonation_target=ImpersonationTarget.BANK,
        urgency=0.9, fear=0.8, authority_pressure=0.8, credential_request=True, payment_request=True,
        payment_method=PaymentMethod.UPI, requested_action="Update KYC",
        social_engineering_tactics=[SocialEngineeringTactic.URGENCY_PRESSURE], target_type="individual",
        extraction_confidence=0.95, upi_ids=["shared@ybl"]
    )

    dna2 = ScamDNA(
        language="en", channel=IncidentChannel.SMS, impersonation_target=ImpersonationTarget.BANK,
        urgency=0.9, fear=0.8, authority_pressure=0.8, credential_request=True, payment_request=True,
        payment_method=PaymentMethod.UPI, requested_action="Update KYC",
        social_engineering_tactics=[SocialEngineeringTactic.URGENCY_PRESSURE], target_type="individual",
        extraction_confidence=0.95, upi_ids=["shared@ybl"]
    )

    inc1 = Incident(raw_text="Inc 1", channel=IncidentChannel.SMS, scam_dna=dna1)
    inc2 = Incident(raw_text="Inc 2", channel=IncidentChannel.SMS, scam_dna=dna2)

    rel = engine.evaluate_pair(inc1, inc2)
    assert rel is not None
    assert rel.relationship_confidence >= 0.60
    assert rel.is_verified
    assert any(e.type.value == "OBSERVED" for e in rel.supporting_evidence)
