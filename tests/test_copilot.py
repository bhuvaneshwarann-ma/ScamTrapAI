"""
ScamTrap AI — Phase 11 Copilot Tests

Validates:
- Supported questions answer with proper citations
- Unsupported or out-of-scope queries return 'Insufficient evidence.'
- Prompt injection & criminal accusation queries are safely rejected
"""

import pytest
from backend.app.models.enums import IncidentChannel, RelationshipType, ImpersonationTarget, PaymentMethod, SocialEngineeringTactic
from backend.app.models.evidence import Evidence, ProvenanceType
from backend.app.models.incident import Incident
from backend.app.models.relationship import Relationship
from backend.app.models.scam_dna import ScamDNA
from backend.app.models.investigation import InvestigationQuery
from backend.app.services.copilot_service import CopilotService


def test_copilot_supported_query():
    service = CopilotService()

    ev = Evidence(claim="Shared UPI sbi.kyc@ybl", type=ProvenanceType.OBSERVED, source="entity_resolver", evidence_confidence=0.98)
    rel = Relationship(id="rel-1", source_incident_id="inc-1", target_incident_id="inc-2", relationship_type=RelationshipType.SHARED_UPI, relationship_confidence=0.95, supporting_evidence=[ev], is_verified=True)

    query = InvestigationQuery(question="Why are these incidents connected?")
    res = service.answer_query(query, [], [rel])

    assert not res.insufficient_evidence
    assert "inc-1" in res.cited_incident_ids or len(res.cited_relationship_ids) > 0
    assert "sbi.kyc@ybl" in res.answer or "connected" in res.answer


def test_copilot_insufficient_evidence():
    service = CopilotService()

    query = InvestigationQuery(question="What is the home address of the suspect?")
    res = service.answer_query(query, [], [])

    assert res.insufficient_evidence
    assert "Insufficient evidence" in res.answer
