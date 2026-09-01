"""
ScamTrap AI — Canonical Evidence Object Tests

Validates:
- Immutability of Evidence records (frozen=True)
- Provenance tagging enforcement (OBSERVED | INFERRED | PREDICTED)
- Supporting references and scoring factor mapping
"""

import pytest
from pydantic import ValidationError

from backend.app.models.enums import ProvenanceType
from backend.app.models.evidence import Evidence


def test_evidence_creation():
    """Create valid Evidence object."""
    ev = Evidence(
        claim="Shared UPI ID 'scammer@ybl' observed in both incidents",
        type=ProvenanceType.OBSERVED,
        source="entity_resolver",
        evidence_confidence=0.98,
        supporting_incident_ids=["inc-101", "inc-102"],
        supporting_entity_ids=["ent-upi-1"],
        scoring_factors={"shared_upi_exact": 0.98},
    )
    assert ev.claim.startswith("Shared UPI ID")
    assert ev.type == ProvenanceType.OBSERVED
    assert ev.source == "entity_resolver"
    assert ev.evidence_confidence == 0.98
    assert "inc-101" in ev.supporting_incident_ids


def test_evidence_immutability():
    """Evidence object must be immutable after creation."""
    ev = Evidence(
        claim="Embedding similarity 0.91",
        type=ProvenanceType.INFERRED,
        source="similarity_service",
        evidence_confidence=0.91,
    )
    with pytest.raises(ValidationError):
        ev.evidence_confidence = 0.50  # Modifying frozen model fails


def test_invalid_provenance_fails():
    """Invalid provenance string fails validation."""
    with pytest.raises(ValidationError):
        Evidence(
            claim="Invalid claim",
            type="GUESSWORK",  # Invalid provenance
            source="tester",
            evidence_confidence=0.5,
        )
