"""
ScamTrap AI — Phase 10 Explainability Tests

Validates:
- Strict provenance separation (OBSERVED / INFERRED / PREDICTED)
- Inferred information is never converted to observed facts
- Legal/criminal disclaimer is present
"""

import pytest
from backend.app.models.enums import ProvenanceType, RelationshipType
from backend.app.models.evidence import Evidence
from backend.app.models.relationship import Relationship
from backend.app.services.evidence_service import EvidenceService


def test_explain_relationship_provenance():
    service = EvidenceService()

    ev1 = Evidence(claim="Same UPI ID sbi.kyc.update@ybl", type=ProvenanceType.OBSERVED, source="entity_resolver", evidence_confidence=0.98)
    ev2 = Evidence(claim="ScamDNA similarity 0.91", type=ProvenanceType.INFERRED, source="similarity_service", evidence_confidence=0.91)

    rel = Relationship(
        source_incident_id="inc-1",
        target_incident_id="inc-2",
        relationship_type=RelationshipType.SHARED_UPI,
        relationship_probability=0.92,
        relationship_confidence=0.95,
        supporting_evidence=[ev1, ev2],
        is_verified=True,
    )

    explanation = service.explain_relationship(rel)

    assert explanation["is_verified"]
    assert "Same UPI ID sbi.kyc.update@ybl" in explanation["provenance_breakdown"]["observed"]
    assert "ScamDNA similarity 0.91" in explanation["provenance_breakdown"]["inferred"]
    assert len(explanation["provenance_breakdown"]["observed"]) == 1
    assert "DISCLAIMER" in explanation["disclaimer"]
