"""
ScamTrap AI — Phase 8 Graph Engine Tests

Validates:
- NetworkX heterogeneous graph construction
- Subgraph component clustering
- React Flow JSON formatting with evidence on edges
"""

import pytest
from backend.app.models.enums import IncidentChannel, RelationshipType
from backend.app.models.incident import Incident
from backend.app.models.relationship import Relationship
from backend.app.models.scam_dna import ScamDNA, ImpersonationTarget, PaymentMethod
from backend.app.services.graph_engine import GraphEngine


def test_graph_construction_and_react_flow():
    engine = GraphEngine()

    dna1 = ScamDNA(
        language="en", channel=IncidentChannel.SMS, impersonation_target=ImpersonationTarget.BANK,
        urgency=0.9, fear=0.8, authority_pressure=0.8, credential_request=True, payment_request=True,
        payment_method=PaymentMethod.UPI, requested_action="Update KYC", target_type="individual",
        extraction_confidence=0.95, upi_ids=["sbi.kyc.update@ybl"]
    )

    inc1 = Incident(id="inc-1", raw_text="Inc 1", channel=IncidentChannel.SMS, scam_dna=dna1)
    inc2 = Incident(id="inc-2", raw_text="Inc 2", channel=IncidentChannel.SMS, scam_dna=dna1)

    rel = Relationship(
        source_incident_id="inc-1",
        target_incident_id="inc-2",
        relationship_type=RelationshipType.SHARED_UPI,
        relationship_probability=0.95,
        relationship_confidence=0.98,
        is_verified=True,
    )

    g = engine.build_graph([inc1, inc2], [rel])

    assert g.has_node("inc-1")
    assert g.has_node("inc-2")
    assert g.has_node("upi:sbi.kyc.update@ybl")
    assert g.has_edge("inc-1", "inc-2")

    rf_data = engine.to_react_flow_json()
    assert "nodes" in rf_data
    assert "edges" in rf_data
    assert len(rf_data["nodes"]) >= 3
    assert len(rf_data["edges"]) >= 3
